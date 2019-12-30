
import pandas as pd
from scipy import sparse, ndimage
from sklearn.utils.extmath import safe_sparse_dot

from nilearn import datasets, input_data, image

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']

save_path = '.'

icbm = datasets.fetch_icbm152_2009()

for i, roi in enumerate([64, 128, 256, 512, 1024]):
    difumo = fetch_difumo(dimension=roi)

    d_img = image.load_img(difumo.maps)
    dd = d_img.get_data()
    data = dd.reshape([-1, dd.shape[-1]]).T
    data = sparse.csr_matrix(data)

    if i == 0:
        masks = image.load_img([icbm.gm, icbm.wm, icbm.csf])
        masks = image.resample_to_img(image.load_img([icbm.gm,
                                                      icbm.wm,
                                                      icbm.csf]),
                                      d_img)
        m = masks.get_data()
        m = m.reshape([-1, 3])
        m = sparse.csr_matrix(m)
    overlaps = safe_sparse_dot(data, m, dense_output=True)
    df = pd.DataFrame(overlaps, columns=['GM', 'WM', 'CSF'])
    to_csv = pd.concat([difumo.labels, df], axis=1)
    to_csv.to_csv(save_path.format(roi), index=False)
