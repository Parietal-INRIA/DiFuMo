import os
from os.path import join
from nilearn import plotting
from nilearn.image import iter_img

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']


import bs4


for n in [64, 128, 256, 512, 1024]:
    data = fetch_difumo(dimension=n)
    labels = data.labels
    maps_img = data.maps

    save_dir = join('..', str(n), 'html')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for i, (img, label) in enumerate(zip(iter_img(maps_img),
                                         labels['names'])):
        cut_coords = plotting.find_xyz_cut_coords(img)
        html_view = plotting.view_img(img, cut_coords=cut_coords,
                                      colorbar=False)

        # Post-processing the HTML
        soup = bs4.BeautifulSoup(html_view.get_standalone(),
                                 'html.parser')
        # Add CSS in the header
        style = soup.new_tag('style')
        style.append("""
            body {
                background: black;
                color: white;
                font-family: arial;
            }

            h1 {
                font-size: xxx-large;
                margin-bottom: 0px;
            }

            a:link {
                background-color: lightgreen;
                font-size: 25px;
            }
        """)
        soup.head.append(style)
        #soup.head.title.string = label
        title = soup.new_tag('h1')
        title.append(label)
        soup.body.insert(0, title)

        link = ("https://parietal-inria.github.io/DiFuMo/"
                "{0}/related/component_{1}")
        new_link = soup.new_tag('a', href=link.format(n, i + 1))
        new_link.string = "related brain structures"
        soup.html.append(new_link)
        soup.body.insert(3, new_link)

        html_doc = str(soup)

        file_name = join(save_dir, '{0}.html'.format(i + 1))
        with open(file_name, 'wb') as f:
            f.write(html_doc.encode('utf-8'))
