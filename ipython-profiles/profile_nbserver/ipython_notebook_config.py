import os
import sys

if os.name == 'posix':
    nbdir = '~/notebooks'
elif os.name == 'nt':
    nbdir = '~/Dropbox/Notebooks'

nbdir = os.path.expanduser(nbdir)
nbdir = os.path.normpath(nbdir)

sys.path.append(nbdir)

c = get_config()
load_subconfig('ipython_config.py', profile='sympy')
load_subconfig('ipython_notebook_config.py', profile='sympy')

c.InteractiveShellApp.exec_lines.append("import numpy as np")
c.InteractiveShellApp.exec_lines.append("import scipy as sp")
c.InteractiveShellApp.exec_lines.append("import pandas as pd")
c.InteractiveShellApp.exec_lines.append("import matplotlib.pyplot as plt")

c.InteractiveShellApp.extensions.append('nbtoc')

c.IPKernelApp.matplotlib = 'inline'
c.InlineBackend.figure_format = 'svg'

c.NotebookManager.notebook_dir = nbdir

c.NotebookApp.open_browser = False

c.NotebookManager.save_script = True

if os.name == 'nt':
    c.IPythonWidget.font_family = 'DejaVu Sans Mono'
