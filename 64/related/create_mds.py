import numpy as np
import mdutils

n_components = 64
write_line = '![{0}]({0}.jpg "Structures overlap with component_{0}")'

for idx in np.arange(n_components) + 1:
    print(idx)
    mdFile = mdutils.MdUtils(file_name='component_' + str(idx))
    mdFile.write(write_line.format(idx))
    mdFile.create_md_file()
