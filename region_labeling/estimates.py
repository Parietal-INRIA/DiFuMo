"""
Author: Jerome Dockes
        Kamalaker Dadi (documentation)
"""
import numpy as np
import pandas as pd

from scipy import sparse
from sklearn.utils.extmath import safe_sparse_dot
from sklearn.preprocessing import LabelBinarizer

from nilearn import image


def overlaps(queries, targets=None):
    """Overlaps between regions provided as sparse or dense matrices

    Parameters
    ----------
    queries : scipy.sparse.csr_matrix
        Sparse/dense matrix transformed from Nifti file of
        DiFuMo atlas (4D).

    targets : str, Nifti-image like
        Pre-defined atlas to measure the overlap for DiFuMo
        atlas labeling.

    Returns
    -------
    data : dict
        With keys:
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
    if targets is None:
        targets = queries
    intersections = safe_sparse_dot(queries, targets.T)
    target_sizes = np.asarray(targets.sum(axis=1)).ravel()
    n_targets = len(target_sizes)
    ts_matrix = sparse.dia_matrix((1 / np.maximum(target_sizes, 1), 0),
                                  shape=(n_targets, n_targets))
    overlap_proportion = safe_sparse_dot(intersections, ts_matrix)
    overlap = sparse.lil_matrix(intersections)
    overlap = [
        pd.Series(d, index=r).sort_values(ascending=False)
        for (r, d) in zip(overlap.rows, overlap.data)
    ]
    overlap_proportion = sparse.lil_matrix(overlap_proportion)
    overlap_proportion = [
        pd.Series(d, index=r).sort_values(ascending=False)
        for (r, d) in zip(overlap_proportion.rows, overlap_proportion.data)
    ]
    return {
        'intersection': intersections,
        'target_size': target_sizes,
        'overlap_proportion': overlap_proportion,
        'overlap_size': overlap,
    }


def labels_img_to_binary(labels_img, labels, masker):
    """Transform an atlas image of label indices into binary masks

    Pre-processing steps include:
        1. resampling
        2. Encoding atlas image into sparse matrix using LabelBinarizer

    Parameters
    ----------
    labels_img : Nifti-image like
        Prepare atlas image for estimating overlaps.

    labels : list of str
        Anatomical names assigned to each label

    masker : instance of NiftiMasker
        Requires to transform Nifti-image to data

    Returns
    -------
    encoded : sparse matrix
        Encoded atlas image using LabelBinarizer.

    new_labels : list of str
        Anatomical names
    """
    labels_img = image.resample_to_img(
        labels_img, masker.mask_img_, interpolation='nearest')
    labels_data = masker.transform(labels_img).squeeze().astype(int)
    encoder = LabelBinarizer(sparse_output=True)
    encoded = encoder.fit_transform(labels_data).T
    new_labels = np.asarray(labels)[encoder.classes_]
    return encoded, new_labels
