"""
"""
import os
from os.path import join
import nibabel

from matplotlib import pyplot as plt

from nilearn import image, plotting

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']



def _plot_dl_maps(img, cut_coords, annotated_name,
                  index, dimension):
    display = plotting.plot_stat_map(stat_map_img=img, cut_coords=cut_coords, 
                                     colorbar=False, black_bg=False)
    save_dir = join('..', str(dimension), 'final')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(join(save_dir, '{0}.jpg'.format(index)),
                bbox_inches='tight', facecolor='w')
    plt.close()
    return display


def _save_results(annotated_names, maps_img, dimension):
    maps_img = nibabel.load(maps_img)
    for i, img in enumerate(image.iter_img(maps_img)):
        cut_coords = plotting.find_xyz_cut_coords(img)
        if annotated_names is not None:
            annotated_name = annotated_names.iloc[i].names
        else:
            annotated_name = None
        _plot_dl_maps(img, cut_coords, annotated_name, i, dimension)
    return


if __name__ == '__main__':
    for n in [64, 128, 256, 512, 1024]:
        data = fetch_difumo(dimension=n)
        annotated_names = data.labels
        _save_results(annotated_names, data.maps, n)
