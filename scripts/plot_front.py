"""
"""
import os
from os.path import join
import matplotlib
import matplotlib.pyplot as plt

from nilearn.image import iter_img
from nilearn import plotting

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']


def _get_values(maps_img, percent):
    """Get new intensities in each probabilistic map specified by
       value in percent. Useful for visualizing less non-overlapping
       between each probabilistic map.

    Parameters
    ----------
    maps_img : 4D Nifti image
        A 4D image which contains each dictionary/map in 3D.

    percent : float
        A value which is multiplied by true values in each probabilistic
        map.

    Returns
    -------
    values : list
        Values after multiplied by percent.
    """
    values = []
    for img in iter_img(maps_img):
        values.append(img.get_data().max() * percent)
    return values


display_mode = 'xz'
cut_coords = [46, 20]
percent = 0.33
cmap = matplotlib.colors.ListedColormap('k', name='from_list', N=256)

components_to_display = [64, 128, 256, 512, 1024]

for i, n_components in enumerate(components_to_display):
    maps_img = fetch_difumo(dimension=n_components).maps
    if percent is not None:
        threshold = _get_values(maps_img, percent)
    else:
        threshold = None
    display = plotting.plot_prob_atlas(maps_img,
                                       threshold=threshold, dim=0.1,
                                       draw_cross=False, cut_coords=cut_coords,
                                       display_mode=display_mode,
                                       cmap=cmap, linewidths=1.5)
    save_dir = join('imgs', 'front')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(join(save_dir, '{0}.jpg'.format(n_components)),
                bbox_inches='tight')
