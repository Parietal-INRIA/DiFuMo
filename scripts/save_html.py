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
    new_div = soup.new_tag('div', attrs={'class': 'box flush_right'})

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


def _add_back_2_components(soup, n):
    """Add back to all components link to soup body
    """
    link_to_components = ("https://parietal-inria.github.io/"
                          "DiFuMo/{0}".format(n))
    new_div = soup.new_tag('div', attrs={'class': 'box flush_right'})

    add_link_back_to_components = soup.new_tag(
            "a", attrs={"href": link_to_components,
                        "class": "back"})
    label = u"All DiFuMo-{0} maps \U0001F517".format(n)
    add_link_back_to_components.string = label
    new_div.append(add_link_back_to_components)
    link = soup.new_tag(
            "a", attrs={"href": link_to_components,
                        "class": "back"})
    img = soup.new_tag(
            'img', attrs={"src": "../../imgs/display_maps/{0}.jpg".format(n),
                          "width": "90%"},
            )
    link.append(img)
    new_div.append(link)
    soup.body.insert(4, new_div)
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
    new_div = soup.new_tag('div', attrs={'class': 'box flush_left'})
    new_tag = soup.new_tag('h3')
    new_tag.append("Neighboring DiFuMo maps")
    new_div.append(new_tag)
    for dim in overlaps_in_n:
        new_header = soup.new_tag('h4')
        new_header.append("Dim " + str(dim))
        new_div.append(new_header)
        grab_identified = this_n[this_n['overlap_against'] == dim]
        grab_i = grab_identified[grab_identified['component'] == i + 1]
        tab = soup.new_tag('table')
        for other_i in grab_i['identified'].values:
            row = soup.new_tag('tr')
            cell1 = soup.new_tag('td')
            add_link_difumo_overlap = soup.new_tag(
                    'a', href=link_to_difumo_overlap.format(dim, other_i))
            label = grab_i[grab_i['identified'] == other_i].label.values[0]
            add_link_difumo_overlap.string = label
            cell1.append(add_link_difumo_overlap)
            row.append(cell1)
            tab.append(row)
        new_div.append(tab)
    soup.body.insert(position, new_div)
    return soup


def _add_names_of_the_similar_labels(soup, close_labels, position):
    """ Add links to structures with similar names """
    link_to_difumo = ("https://parietal-inria.github.io/DiFuMo/"
                      "{0}/html/{1}.html")
    new_div = soup.new_tag('div', attrs={'class': 'box flush_left'})
    new_tag = soup.new_tag('h3')
    new_tag.append("Similarly-named DiFuMo maps")
    new_div.append(new_tag)
    tab = soup.new_tag('table')
    for _, label in close_labels.iterrows():
        row = soup.new_tag('tr')
        cell1 = soup.new_tag('td')
        dim = label['dimension']
        other_i = label['index']
        add_link_difumo_overlap = soup.new_tag(
                'a', href=link_to_difumo.format(dim, other_i))
        name = label['names']
        add_link_difumo_overlap.string = '%s (dim %i)' % (name, dim)
        cell1.append(add_link_difumo_overlap)
        row.append(cell1)
        tab.append(row)
    new_div.append(tab)
    soup.body.insert(position, new_div)
    return soup, position + 1


# Find the closest matching strings
all_labels = []

for n in [64, 128, 256, 512, 1024]:
    labels = fetch_difumo(dimension=n).labels
    labels['dimension'] = n
    labels = labels.reset_index()
    all_labels.append(labels)

all_labels = pd.concat(all_labels)

from sklearn.feature_extraction import text
from sklearn import neighbors
vectorizer = text.CountVectorizer(analyzer='char_wb', ngram_range=[5, 5])
labels_vec = vectorizer.fit_transform(all_labels['names'])
nn = neighbors.NearestNeighbors(p=1, n_neighbors=7)
nn.fit(labels_vec)

# Do all HTML files
#for n in [64, 128, 256, 512, 1024]:
for n in [512, ]:
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
            h3, h2 {
                margin: 1px;
            }
            h4 {
                margin-bottom: 1px;
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
                font-size: 20px;
                display: table-row;
                max-width: 25ex;
            }
            .back img {
                max-width: 100%;
            }
            div {
                font-size: 20px;
            }
            div.flush_right {
                float: right;
            }
            div.flush_left {
                float: left;
            }
            div.box {
                background: white;
                display: grid;
                color: black;
                padding: 5px;
                border-radius: 5px;
                margin: 10px;
            }
        """)
        soup.head.append(style)
        soup.head.title.string = "{0} (DiFuMo-{1})".format(label, n)
        title = soup.new_tag('h1')
        title.append(label)
        soup.body.insert(0, title)

        # add related anatomical structures
        names = related_names[related_names['component'] == i]
        soup, position = _add_names_of_the_related_structures(soup,
                                                              names)
        # Add link back to components
        soup = _add_back_2_components(soup, n)

        # Add links to DiFuMo overlaps
        soup = _add_links_to_difumo_overlaps(soup, n, i, position + 1)
        position += 1

        # Add the strings that are closest
        dist, close_idx = nn.kneighbors(
                    vectorizer.transform([labels['names'].iloc[i]]))
        close_idx = close_idx[dist < 3]
        close_labels = all_labels.iloc[close_idx]
        close_labels = close_labels[close_labels.index != i]
        if len(close_labels):
            soup, position = _add_names_of_the_similar_labels(soup,
                                                            close_labels,
                                                            position + 1)
        html_doc = str(soup)

        file_name = join(save_dir, '{0}.html'.format(i + 1))
        with open(file_name, 'wb') as f:
            f.write(html_doc.encode('utf-8'))
        print('Generated file {0}'.format(file_name))
