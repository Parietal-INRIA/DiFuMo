import os
import pandas as pd
from os.path import join
from nilearn import plotting
from nilearn.image import iter_img

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']


import bs4


# aliases
ATLASES = {'harvard_oxford': 'Harvard Oxford',
           'destrieux': 'Destrieux',
           'mist': 'BASC',
           'juelich': 'Juelich',
           'jhu': 'JHU',
           'diedrichsen': 'Diedrichsen',
           'modl': 'MODL_128'}


def _mask_background(data):
    """Mask out the background information from given data

    Parameters
    ----------
    data : pd.DataFrame
        Data to be masked

    Returns
    -------
    data : pd.DataFrame
        Masked data
    """
    mask = data == 'Background'
    data = data[~mask].dropna(axis=1)
    return data


def _remove_columns(data):
    """Remove irrelevant columns
    """
    columns = data.columns.to_list()
    columns.remove('cut_coords')
    columns.remove('component')
    return columns


def _add_link(soup):
    """Adding soup.new_tag to link to a plotted image which
    visualizes the related anatomical structures to each
    component
    """
    # Add links to visualize an image of related anatomical
    # structures to each component
    link = ("https://parietal-inria.github.io/DiFuMo/"
            "{0}/related/component_{1}")
    new_link = soup.new_tag('a', href=link.format(n, i + 1))
    new_link.string = "related brain structures"
    soup.html.append(new_link)
    soup.body.insert(3, new_link)
    return soup


def _add_names_of_the_related_structures(soup, names):
    """
    """
    position = 4
    masked_names = _mask_background(names)
    columns = _remove_columns(masked_names)
    for atlas in columns:
        match_found = masked_names[atlas].values[0]
        new_tag = soup.new_tag('div')
        new_tag.append(ATLASES[atlas] + ':' + match_found)
        soup.body.insert(position, new_tag)
        position += 1    
    return soup


for n in [128]:
    data = fetch_difumo(dimension=n)
    labels = data.labels
    maps_img = data.maps

    save_dir = join('..', str(n), 'html')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    data_dir = '../region_labeling/{0}.csv'
    related_names = pd.read_csv(data_dir.format(n))
    related_names = related_names.drop('Unnamed: 0',
                                       axis=1)
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
            div {
                font-size: 20px;
            }
        """)
        soup.head.append(style)
        #soup.head.title.string = label
        title = soup.new_tag('h1')
        title.append(label)
        soup.body.insert(0, title)

        # Add new_tag linking an image of related anatomical
        # structures to each component
        soup = _add_link(soup)

        # add related anatomical structures
        names = related_names[related_names['component'] == i]
        soup = _add_names_of_the_related_structures(soup,
                                                    names)

        html_doc = str(soup)

        file_name = join(save_dir, '{0}.html'.format(i + 1))
        with open(file_name, 'wb') as f:
            f.write(html_doc.encode('utf-8'))
