import os

c = get_config()
load_subconfig('ipython_config.py')

if os.name == 'nt':
    c.IPythonWidget.font_family = u'DejaVu Sans Mono'
