
PYTHON ?= python3

all: front links final

front: maps_xz index

maps_xz:
	$(PYTHON) plot_front.py

index:
	$(PYTHON) create_index_md.py

links:
	$(PYTHON) plot_display_maps.py
	$(PYTHON) plot_maps_for_each_dimension.py
	$(PYTHON) save_html.py

final:
	$(PYTHON) create_each_dimension_md.py
