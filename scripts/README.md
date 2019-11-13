# How to build the DiFuMo site

First, images needs to be created for front end displays, these two scripts helps in creating
them fetching atlases from OSF.
1. plot_display_maps.py
2. plot_front.py
3. create_index_md.py for creating main page "index.md"

Next, you need to create 64.md, 128.md, 256.md, 512.md, 1024.md which are linked in "index.md"

To do so, all the components to be plotted and saved using below one:
4. plot_maps_for_each_dimension_md.py 

At the same time, use html script to save all html files.
5. save_html.py

Finally, create all dimension mds
6. create_each_dimension_md.py

Optionnally: regenerate the sitemap for Google indexing
7. create_sitemap.py
