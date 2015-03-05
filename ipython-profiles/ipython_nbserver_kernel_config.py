import os

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

app.exec_lines.append("nbdir = r'%s'" % nbdir)

if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='mathjax')")
