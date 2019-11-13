"""
Generate a sitemap for Google indexing
"""

import glob

sitemap = open('../assets/sitemap.txt', 'w')

for html_file in glob.glob('../*/html/*.html'):
    sitemap.write(html_file)
    sitemap.write('\n')

for md_file in glob.glob('../*.md'):
    sitemap.write(md_file.replace('.md', '.html'))
    sitemap.write('\n')

sitemap.close()
