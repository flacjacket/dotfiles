import os

if os.name == 'nt':
    nbdir = '~/Dropbox/Notebooks'
else:
    nbdir = '~/notebooks'

nbdir = os.path.expanduser(nbdir)
nbdir = os.path.normpath(nbdir)

c = get_config()
app = c.InteractiveShellApp

c.IPKernelApp.matplotlib = 'inline'
c.NotebookApp.notebook_dir = nbdir
c.NotebookApp.open_browser = False
