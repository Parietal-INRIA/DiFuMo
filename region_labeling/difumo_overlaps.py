"""
"""
from os.path import join
import nibabel
import pandas as pd

from nilearn import datasets, input_data, image, plotting

from utils import set_difumo_storage, transform_difumo_to_data
from estimates import overlaps, labels_img_to_binary
from atlas import fetch_atlases
from visualization import plot_overlaps

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']


def find_overlaps(dimension):
    """Estimate overlap (queries) within and across components

    Parameters
    ----------
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
    """
    masker = input_data.NiftiMasker(
        datasets.load_mni152_brain_mask()).fit([])
    queries = transform_difumo_to_data(dimension=dimension,
                                       masker=masker)
    info = {}
    for n in [64, 128, 256, 512, 1024]:
        targets = transform_difumo_to_data(dimension=n,
                                           masker=masker)
        info[n] = overlaps(queries, targets)
    return info


def save_info(info, dimension):
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

    dimension : int
        DiFuMo atlas dimension

    Returns
    -------
    data : pd.DataFrame
    """
    html = "https://parietal-inria.github.io/DiFuMo/{0}/html/{1}.html"
    table = set_difumo_storage()
    maps_img = nibabel.load(fetch_difumo(dimension=dimension).maps)
    for i, img in enumerate(image.iter_img(maps_img)):
        cut_coords = plotting.find_xyz_cut_coords(img)
        for n in [64, 128, 256, 512, 1024]:
            labels = fetch_difumo(dimension=n).labels['names'].to_list()
            # Proportion of overlap with each index of difumo component
            this_img_info = info[n]['overlap_proportion'][i]
            identified_components = this_img_info.index[1:6]
            if len(identified_components) != 0:
                # grabbing the top five from the overlapped list
                for identified_component in identified_components:
                    table['dimension'].append(dimension)
                    table['component'].append(i + 1)
                    table['overlap_against'].append(n)
                    table['identified'].append(identified_component + 1)
                    table['label'].append(labels[identified_component])
    return pd.DataFrame(table)


if __name__ == '__main__':
    for dimension in [64, 128, 256, 512, 1024]:
        info = find_overlaps(dimension)
        table = save_info(info, dimension)
        table.to_csv(str(dimension) + '_dimension_overlap_difumo.csv')
