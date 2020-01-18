import mdutils
import os

dic = {64: "https://osf.io/wjum7/download",
       128: "https://osf.io/kdfg3/download",
       256: "https://osf.io/vza2y/download",
       512: "https://osf.io/a23gw/download",
       1024: "https://osf.io/jpdum/download",
       }

mdFile = mdutils.MdUtils(file_name=os.path.join('..', 'index'))

mdFile.write('# Dictionaries of multiple dimensions')

link_location = "https://parietal-inria.github.io/DiFuMo/{0}"
start_line = '[![{0} dimensions](imgs/front/{0}.jpg "{0} dimensions")]({1})'
# start_line = '![{0} dimensions](imgs/front/{0}.jpg "{0} dimensions")'
next_line = ('See regions for: [{0} dimensions]({0} "Labels '
             'for {0} dimensions") &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')

# Iteration
for n in [64, 128, 256, 512, 1024]:
    link_location = ("https://parietal-inria.github.io/"
                     "DiFuMo/{0}".format(n))
    mdFile.new_paragraph(start_line.format(n,
                                           link_location))
    mdFile.new_paragraph(next_line.format(n))
    mdFile.write('[Download]({0})'.format(dic[n]))

mdFile.create_md_file()
