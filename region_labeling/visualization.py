"""Visualization tools for plotting overlaps
"""
import os
from os.path import join
import numpy as np
import nibabel
from matplotlib import pyplot as plt

from nilearn import plotting, image
from nilearn._utils.niimg_conversions import _safe_get_data

from atlas import fetch_atlases

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']

# aliases
ATLASES = {'harvard_oxford': 'Harvard Oxford',
           'destrieux': 'Destrieux',
           'mist': 'BASC',
           'juelich': 'Juelich',
           'jhu': 'JHU',
           'diedrichsen': 'Diedrichsen',
           'modl': 'MODL_128'}

# Not so great defaults but it works
xy = {'harvard_oxford': {'x': -0.01, 'y': 0.3},
      'destrieux': {'x': -0.01, 'y': 0.4},
      'mist': {'x': -0.01, 'y': 0.4},
      'juelich': {'x': -0.01, 'y': 0.5},
      'jhu': {'x': -0.01, 'y': 0.3},
      'diedrichsen': {'x': -0.01, 'y': 0.4},
      'modl': {'x': -0.01, 'y': 0.38}}


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


def _simplify_grid(fig, axes, i):
    """Collapse double column
    """
    gs = axes[i, 0].get_gridspec()
    for ax in axes[i, 0:]:
        ax.remove()
    axbig = fig.add_subplot(gs[i, 0:])
    return axbig


def _plotting_roi(labels_img, label_match, cut_coords, color,
                  axes, fig, alias):
    """Plotting Regions of interest (ROI)
    """
    plotting.plot_roi(labels_img, cut_coords=cut_coords,
                      black_bg=True,
                      cmap=plotting.cm.alpha_cmap(color,
                                                  alpha_min=1.),
                      annotate=False, axes=axes,
                      figure=fig)
    axes.set_title(alias + ':' + label_match, color='w', fontsize=18)
    return


def _plot_difumo(img, axes, proposed_name, cut_coords, dimension):
    """Plot component-wise DiFuMo atlases
    """
    plotting.plot_stat_map(stat_map_img=img, cut_coords=cut_coords,
                           colorbar=False, black_bg=True, axes=axes)
    title = '{0} {1}: {2}'.format('DiFuMo', dimension, proposed_name)
    axes.set_title(title, color='w', fontsize=18)
    return


def _plot_references(label_match, labels_img, labels, atlas,
                     idx, fig, axes, cut_coords, color):
    """Plot reference atlases in each row
    """
    axes = _simplify_grid(fig, axes, idx + 1)
    labels_data = _safe_get_data(nibabel.load(labels_img))
    if atlas in ['harvard_oxford', 'diedrichsen', 'juelich',
                 'jhu', 'mist']:
        if label_match != 'Background':
            mask = np.where(np.array(labels) == label_match)[0][0]
            data = (labels_data == mask)
            _plotting_roi(image.new_img_like(labels_img,
                                             data),
                          label_match, cut_coords, color,
                          axes, fig, ATLASES[atlas])
        else:
            axes.axis('off')
    else:
        mask = np.where(np.array(labels['name']) == label_match.encode())[0][0]
        data = (labels_data == mask)
        _plotting_roi(image.new_img_like(labels_img,
                                         data),
                      label_match, cut_coords, color,
                      axes, fig, ATLASES[atlas])
    return


def plot_overlaps(info, atlas_names, dimension, output_dir=None,
                  cmap=plt.cm.gist_rainbow, proposed_labels=None):
    """Plot the regions overlapped from existing anatomical atlases

    Parameters
    ----------
    info : pd.DataFrame
        Data frame contains ovelap information of specific dimension
        with regards to : ['harvard_oxford', 'destrieux', 'diedrichsen',
                           'jhu', 'juelich', 'mist', 'component',
                           'cut_coords']
        The info columns

    atlas_names : str or list of str
        Grab atlas from web given the name. Few are shipped with FSL
        and Nilearn.
        Valid options:  ['harvard_oxford', 'destrieux', 'diedrichsen',
                         'juelich', 'jhu', 'mist']

    dimension : int
        DiFuMo atlas dimension

    cmap : instance of matplotlib cmap or str, default='gist_rainbow'
        Look at these link
        https://nilearn.github.io/auto_examples/01_plotting/plot_colormaps.html#sphx-glr-auto-examples-01-plotting-plot-colormaps-py

    output_dir : str
        Path to save the plots

    proposed_labels : pd.DataFrame, optional
        DiFuMo proposed labels useful for comparisons.
    """
    atlases = fetch_atlases(atlas_names)
    cmap = plt.cm.get_cmap(cmap)
    color_list = cmap(np.linspace(0, 1, dimension))
    difumo = fetch_difumo(dimension=dimension)
    maps_img = nibabel.load(difumo.maps)
    if proposed_labels is None:
        proposed_labels = difumo.labels
    for comp_idx, (img, color) in enumerate(zip(image.iter_img(maps_img),
                                                color_list)):
        cut_coords = plotting.find_xyz_cut_coords(img)
        this_data = info[info['component'] == comp_idx]
        masked_data = _mask_background(this_data)
        columns = _remove_columns(masked_data)
        fig, axes = plt.subplots(ncols=2, nrows=len(columns) + 1,
                                 figsize=(10, 18), facecolor='k')
        proposed_label = proposed_labels.iloc[comp_idx].names
        # plot difumo component-wise
        axbig = _simplify_grid(fig, axes, 0)
        _plot_difumo(img, axbig, proposed_label, cut_coords,
                     dimension)
        # plot overlapped references - backbone for naming DiFuMo
        for atlas_idx, atlas in enumerate(columns):
            labels_img, labels = atlases[atlas].maps, atlases[atlas].labels
            # this atlas match for component index
            match_found = masked_data[atlas].values[0]
            _plot_references(match_found, labels_img, labels,
                             atlas, atlas_idx, fig, axes,
                             cut_coords, color)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(join(output_dir,
                         '{0}.jpg'.format(comp_idx + 1)),
                    facecolor='k', bbox_inches='tight')
        plt.close()
    return
