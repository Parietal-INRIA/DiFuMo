import os
from os.path import join
import pandas as pd
from nilearn import plotting
from nilearn.image import iter_img

from fetcher import fetch_difumo

for n in [64, 128, 256, 512, 1024]:
    data = fetch_difumo(dimension=n)
    labels = data.labels
    maps_img = data.maps

    save_dir = join(str(n), 'html')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for i, img in enumerate(iter_img(maps_img)):
        cut_coords = plotting.find_xyz_cut_coords(img)
        html_view = plotting.view_img(img, cut_coords=cut_coords,
                                      title=labels.iloc[i].names,
                                      colorbar=False)
        html_view.save_as_html(join(save_dir, '{0}.html'.format(i + 1)))
