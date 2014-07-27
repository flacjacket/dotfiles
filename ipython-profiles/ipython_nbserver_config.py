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

load_subconfig('ipython_config.py', profile='default')
load_subconfig('ipython_config.py', profile='labwork')

#app.extensions.append('nbtoc')

c.IPKernelApp.matplotlib = 'inline'

#c.InlineBackend.figure_format = 'svg'

c.NotebookManager.notebook_dir = nbdir
c.NotebookManager.save_script = True

c.NotebookApp.open_browser = False

if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='mathjax')")
