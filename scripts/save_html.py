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
    columns = list(data.columns)
    columns.remove('cut_coords')
    columns.remove('component')
    return columns


def _add_names_of_the_related_structures(soup, names):
    """Add names in strings of overlapped anatomical structures
    """
    position = 3
    masked_names = _mask_background(names)
    columns = _remove_columns(masked_names)
    new_div = soup.new_tag('div', attrs={'class': 'box'})

    # Add links to visualize an image of related anatomical
    # structures to each component
    link = ("https://parietal-inria.github.io/DiFuMo/"
            "{0}/related/component_{1}")
    new_header = soup.new_tag('h3')
    new_link = soup.new_tag("a", attrs={"href": link.format(n, i + 1),
                                        "class": "related"})
    new_link.string = "Related brain structures in reference atlases"
    new_header.append(new_link)
    new_div.append(new_header)
    tab = soup.new_tag('table')
    for atlas in columns:
        row = soup.new_tag('tr')
        match_found = masked_names[atlas].values[0]
        cell1 = soup.new_tag('td')
        cell1.append(ATLASES[atlas])
        row.append(cell1)
        cell2 = soup.new_tag('td')
        cell2.append(match_found)
        row.append(cell2)
        tab.append(row)
    new_div.append(tab)
    soup.body.insert(position, new_div)
    return soup, position


def _add_h2(soup):
    """Append and insert heading into soup body
    """
    new_tag = soup.new_tag('h2')
    new_tag.append("Within and across overlaps in DiFuMo "
                   "dimensions")
    soup.body.insert(position, new_tag)
    return soup


def _add_back_2_components(soup, n):
    """Add back to all components link to soup body
    """
    link_to_components = ("https://parietal-inria.github.io/"
                          "DiFuMo/{0}".format(n))
    add_link_back_to_components = soup.new_tag(
            "a", attrs={"href": link_to_components,
                        "class": "back"})
    label = u"All DiFuMo-{0} maps \U0001F517".format(n)
    add_link_back_to_components.string = label
    soup.html.append(add_link_back_to_components)
    soup.body.insert(4, add_link_back_to_components)
    return soup


def _add_links_to_difumo_overlaps(soup, n, i, position):
    """ Add links within and across dimensions for this "n"
    dimension overlap to the body of soup
    """
    link_to_difumo_overlap = ("https://parietal-inria.github.io/DiFuMo/"
                              "{0}/html/{1}.html")
    difumo_path = '../region_labeling/{0}_dimension_overlap_difumo.csv'
    difumo_overlaps = pd.read_csv(difumo_path.format(n))
    this_n = difumo_overlaps[difumo_overlaps['dimension'] == n]
    overlaps_in_n = this_n['overlap_against'].unique()
    for dim in overlaps_in_n:
        position += 1
        new_tag = soup.new_tag('div')
        new_tag.append(str(dim))
        soup.body.insert(position, new_tag)
        grab_identified = this_n[this_n['overlap_against'] == dim]
        grab_i = grab_identified[grab_identified['component'] == i + 1]
        for other_i in grab_i['identified'].values:
            position += 1
            add_link_difumo_overlap = soup.new_tag(
                    'a', href=link_to_difumo_overlap.format(dim, other_i))
            label = grab_i[grab_i['identified'] == other_i].label.values[0]
            add_link_difumo_overlap.string = label
            soup.html.append(add_link_difumo_overlap)
            soup.body.insert(position, add_link_difumo_overlap)
            new_tag = soup.new_tag('div')
            position += 1
            soup.body.insert(position, new_tag)
    return soup


for n in [64, 128, 256, 512, 1024]:
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
                right: 120px;
            }
            h3 {
                margin: 1px;
            }
            .related {
                position: static;
                color: red:
                right: 0;
            }
            a {
                position: relative;
                right: -15px;
                text-decoration: none;
            }
            a:hover {
                color: blue;
                text-decoration: underline;
            }
            tr:nth-child(odd) {
                background-color: #eee;
            }
            .back {
                position: absolute;
                font-size: 20px;
                color: black;
                background: white;
                padding: 5px;
                top: 8px;
                right: 8px;
                border-radius: 4px;
            }
            div {
                font-size: 20px;
            }
            div.box {
                background: white;
                display: table;
                color: black;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        soup.head.append(style)
        soup.head.title.string = label
        title = soup.new_tag('h1')
        title.append(label)
        soup.body.insert(0, title)

        # add related anatomical structures
        names = related_names[related_names['component'] == i]
        soup, position = _add_names_of_the_related_structures(soup,
                                                              names)

        # Add heading for DiFuMo overlaps
        soup = _add_h2(soup)

        # Add links to DiFuMo overlaps
        soup = _add_links_to_difumo_overlaps(soup, n, i, position + 1)

        # Add link back to components
        soup = _add_back_2_components(soup, n)

        html_doc = str(soup)

        file_name = join(save_dir, '{0}.html'.format(i + 1))
        with open(file_name, 'wb') as f:
            f.write(html_doc.encode('utf-8'))
        stop
