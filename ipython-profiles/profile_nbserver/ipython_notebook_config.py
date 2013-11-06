import os
import sys

if os.name == 'nt':
    nbdir = '~/Dropbox/Notebooks'
else:
    nbdir = '~/notebooks'

nbdir = os.path.expanduser(nbdir)
nbdir = os.path.normpath(nbdir)

sys.path.append(nbdir)

c = get_config()
app = c.InteractiveShellApp

load_subconfig('ipython_config.py', profile='sympy')
load_subconfig('ipython_notebook_config.py', profile='sympy')

#app.extensions.append('nbtoc')

c.IPKernelApp.matplotlib = 'inline'

c.InlineBackend.figure_format = 'svg'

c.NotebookManager.notebook_dir = nbdir
c.NotebookManager.save_script = True

c.NotebookApp.open_browser = False

if os.name == 'nt':
    c.IPythonWidget.font_family = 'DejaVu Sans Mono'
