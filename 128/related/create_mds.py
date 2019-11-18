import numpy as np
import mdutils

# Load a file not on the path
import runpy
fetcher = runpy.run_path('../../notebook/fetcher.py')
fetch_difumo = fetcher['fetch_difumo']

n_components = 128
labels = fetch_difumo(dimension=n_components).labels

title = "Structures related to DiFuMo 128 {0}"

write_line = '![{0}]({0}.jpg "{1}")'

link_back_line = ("[Go back to corresponding component]"
                  "(https://parietal-inria.github.io/DiFuMo/128/html/{0}.html)")

for idx, label in zip(np.arange(n_components) + 1,
                      labels['names']):
    mdFile = mdutils.MdUtils(file_name='component_' + str(idx))
    title_ = title.format(label)
    mdFile.write("## " + title_)
    mdFile.new_paragraph(write_line.format(idx, title_))
    mdFile.new_paragraph(link_back_line.format(idx))
    mdFile.create_md_file()
