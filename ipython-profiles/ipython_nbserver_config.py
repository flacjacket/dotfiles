import os
import sys

if os.name == 'nt':
    nbdir = '~/Dropbox/Notebooks'
else:
    nbdir = '~/notebooks'

nbdir = os.path.expanduser(nbdir)
nbdir = os.path.normpath(nbdir)

c = get_config()
app = c.InteractiveShellApp

load_subconfig('ipython_config.py', profile='labwork')

c.IPKernelApp.matplotlib = 'inline'

c.NotebookManager.notebook_dir = nbdir
c.NotebookManager.save_script = True

c.NotebookApp.open_browser = False

app.exec_lines.append("nbdir = r'%s'" % nbdir)

if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='mathjax')")
