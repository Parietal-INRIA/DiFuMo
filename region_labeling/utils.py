"""Supporting functions for recording components overlap with pre-defined
   literature

Author: Kamalaker Dadi, Jerome Dockes
"""
from scipy import sparse

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']


def set_data_storage():
    """ Prepare dictionary with list of pre-defined brain atlas
    attributes to record region labels of most overlap.

    This is useful at the end for making pandas data frame. Then,
    these attributes become column names of data frame.

    Parameters
    ----------
    columns : list of str
        To assign name of the atlas as column attribute

    Returns
    -------
    table : dict
        An empty list with atlas name is returned. Useful for appending
        labels corresponding to most overlapped regions from an atlas.

    """
    columns = ['harvard_oxford', 'destrieux', 'diedrichsen', 'jhu',
               'juelich', 'mist', 'yeo_networks7', 'yeo_networks17',
               'component', 'cut_coords']
    table = {}
    if isinstance(columns, str):
        columns = [columns, ]
    for col in columns:
        table.setdefault(col, [])
    return table


def set_difumo_storage():
    """ Prepare dictionary with list of column attributes to record
    overlap information.

    Returns
    -------
    table : dict
        An empty list with column is returned. Useful for appending
        information corresponding to most overlapped regions from an
        atlas.
    """
    columns = ['dimension', 'component', 'identified', 'overlap_against',
               'label']
    table = {}
    if isinstance(columns, str):
        columns = [columns, ]
    for col in columns:
        table.setdefault(col, [])
    return table


def transform_difumo_to_data(dimension, masker):
    """Transform DiFuMo atlas to sparse matrix

    Parameters
    ----------
    dimension : int
        A DiFuMo atlas is downloaded from OSF of specified
        dimension. Valid options {64, 128, 256, 512, 1024}.

    masker : instance of NiftiMasker
        See nilearn.input_data.NiftiMasker

    Returns
    -------
    queries : scipy.sparse.csr_matrix
        Sparse/dense matrix transformed from Nifti file of
        DiFuMo atlas (4D).
    """
    maps_img = fetch_difumo(dimension=dimension).maps
    maps_data = masker.transform(maps_img).squeeze()
    queries = sparse.csr_matrix(maps_data)
    return queries
