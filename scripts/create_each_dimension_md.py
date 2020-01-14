import numpy as np
import mdutils
import os

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']

dic = {64: "https://osf.io/vfhk8/download",
       128: "https://osf.io/hwc4b/download",
       256: "https://osf.io/ynqu9/download",
       512: "https://osf.io/xcb9g/download",
       1024: "https://osf.io/pxvw2/download",
       }

for n in [64, 128, 256, 512, 1024]:
    n_components = n
    mdFile = mdutils.MdUtils(file_name=os.path.join('..',
                                                    str(n_components)))
    mdFile.write('| All {} components |'.format(n_components))
    mdFile.new_line()
    mdFile.write('|:---:|')
    mdFile.new_line()
    l = '| [![All components](imgs/display_maps/{0}.jpg "All {0} components")]({1})'
    mdFile.write(l.format(n_components, dic[n]))

    data = fetch_difumo(dimension=n_components)
    annotated_names = data.labels

    iter_line = '| Component {0}: {1} |'
    second_line = '|:---:|'
    iter_third_line = ('| [![Component {0}: {1}]'
                       '({3}/final/{2}.jpg "Component {0}: {1}")]'
                       '({3}/html/{0}.html)|')

    for idx in np.arange(n_components) + 1:
        this_name = annotated_names.iloc[idx - 1].Difumo_names
        mdFile.new_paragraph(iter_line.format(idx, this_name))
        mdFile.new_line()
        mdFile.write(second_line)
        mdFile.new_line()
        mdFile.write(iter_third_line.format(idx, this_name, idx - 1, n_components))
    mdFile.create_md_file()
