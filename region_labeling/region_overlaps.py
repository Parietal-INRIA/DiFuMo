"""
"""
from os.path import join
import nibabel
import pandas as pd

from nilearn import datasets, input_data, image, plotting

from utils import set_data_storage, transform_difumo_to_data
from estimates import overlaps, labels_img_to_binary
from atlas import fetch_atlases
from visualization import plot_overlaps

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']


def find_overlaps(atlas_names, dimension):
    """Estimate overlap (queries) provided atlas names

    Parameters
    ----------
    atlas_names : str or list of str
        Grab atlas from web given the name. Few are shipped with FSL
        and Nilearn.
        Valid options:  ['harvard_oxford', 'destrieux', 'diedrichsen',
                         'juelich', 'jhu', 'mist']

    dimension : int
        Dimension of the DiFuMo atlas (4D).

    Returns
    -------
    info : dict
        Contains meta-data assigned to each atlas name such as
        overlap proportion, etc
        Each atlas dict contains following attributes:
            'intersection' : sparse matrix
                dot product between DiFuMo regions and regions in target
                atlas (existing pre-defined)

            'target_size' : np.ndarray
                Size of each region estimated in target atlas

            'overlap_proportion' : list of pd.Series
                Each list contains the proportion of overlap estimated
                between this region and all region in target sizes.
                Sorted according to most strong hit in the overlap.

            'overlap_size' : list
                Each list contain overlap in estimated sizes for all
                regions in target atlas.

    save_labels : dict
        List of original labels specific to each atlas. Useful
        for matching the overlap for the visualization of
        records.
    """
    masker = input_data.NiftiMasker(
        datasets.load_mni152_brain_mask()).fit([])
    queries = transform_difumo_to_data(dimension=dimension,
                                       masker=masker)
    atlases = fetch_atlases(atlas_names)
    info = {}
    save_labels = {}
    for atlas in atlas_names:
        this_atlas = atlases[atlas]
        labels_img, labels = labels_img_to_binary(this_atlas.maps,
                                                  this_atlas.labels,
                                                  masker)
        save_labels[atlas] = labels
        info[atlas] = overlaps(queries, labels_img)
    return info, save_labels


def save_info(info, save_labels, atlas_names, dimension):
    """Save found records

    Parameters
    ----------
    info : dict
        Contains meta-data assigned to each atlas name such as
        overlap proportion, etc
        Each atlas dict contains following attributes:
            'intersection' : sparse matrix
                dot product between DiFuMo regions and regions in target
                atlas (existing pre-defined)

            'target_size' : np.ndarray
                Size of each region estimated in target atlas

            'overlap_proportion' : list of pd.Series
                Each list contains the proportion of overlap estimated
                between this region and all region in target sizes.
                Sorted according to most strong hit in the overlap.

            'overlap_size' : list
                Each list contain overlap in estimated sizes for all
                regions in target atlas.

    save_labels : dict
        List of original labels specific to each atlas. Useful
        for matching the overlap for the visualization of
        records.

    atlas_names : str or list of str
        Grab atlas from web given the name. Few are shipped with FSL
        and Nilearn.
        Valid options:  ['harvard_oxford', 'destrieux', 'diedrichsen',
                         'juelich', 'jhu', 'mist']

    dimension : int
        DiFuMo atlas dimension

    Returns
    -------
    data : pd.DataFrame
    """
    table = set_data_storage()
    maps_img = nibabel.load(fetch_difumo(dimension=dimension).maps)
    for i, img in enumerate(image.iter_img(maps_img)):
        cut_coords = plotting.find_xyz_cut_coords(img)
        table['cut_coords'].append(cut_coords)
        table['component'].append(i)
        for atlas in atlas_names:
            # Proporting of overlap with each index of difumo component
            this_atlas_info = info[atlas]['overlap_proportion'][i]
            if atlas in ['harvard_oxford', 'diedrichsen', 'juelich',
                         'jhu', 'mist']:
                if len(this_atlas_info.index[:1]) != 0:
                    # grabbing the top one from the overlapped list
                    this_label = save_labels[atlas][this_atlas_info.index[:1]][0]
                else:
                    this_label = 'none'
                if atlas == 'mist':
                    table[atlas].append(this_label[0])
                else:
                    table[atlas].append(this_label)
            else:
                this_label = save_labels[atlas][this_atlas_info.index[:1]][0][1]
                this_label = this_label.decode()
                table[atlas].append(this_label)
    return pd.DataFrame(table)


if __name__ == '__main__':
    atlas_names = ['harvard_oxford', 'destrieux', 'diedrichsen',
                   'juelich', 'jhu', 'mist']
    for dimension in [64, 128, 256, 512]:
        info, save_labels = find_overlaps(atlas_names, dimension)
        table = save_info(info, save_labels, atlas_names,
                          dimension)
        table.to_csv(str(dimension) + '.csv')
        plot_overlaps(info=table, atlas_names=atlas_names,
                      dimension=dimension,
                      output_dir=join('..', str(dimension),
                                      'related'))
