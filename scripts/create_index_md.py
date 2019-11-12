import mdutils
import os

mdFile = mdutils.MdUtils(file_name=os.path.join('..', 'index'))

mdFile.write('# Dictionaries of multiple dimensions')

start_line = '![{0} dimensions](imgs/front/{0}.jpg "{0} dimensions")'
next_line = 'See regions for: [{0} dimensions]({0} "Labels for {0} dimensions")'

# Iteration
for n in [64, 128, 256, 512, 1024]:
    mdFile.new_paragraph(start_line.format(n))
    mdFile.new_paragraph(next_line.format(n))

mdFile.create_md_file()
