import os
import sys

if os.name == 'nt':
    nbdir = 'D:/Dropbox/Notebooks'
else:
    nbdir = '~/notebooks'

nbdir = os.path.expanduser(nbdir)
nbdir = os.path.normpath(nbdir)

c = get_config()
app = c.InteractiveShellApp

load_subconfig('ipython_config.py')

c.IPKernelApp.matplotlib = 'inline'

app.exec_lines.append('import os')
app.exec_lines.append('import numpy as np')
app.exec_lines.append('import scipy as sp')
app.exec_lines.append('import pandas as pd')
app.exec_lines.append('import matplotlib as mpl')
app.exec_lines.append('import matplotlib.pyplot as plt')
app.exec_lines.append("nbdir = r'%s'" % nbdir)

app.exec_lines.append("from sympy import init_printing")

if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='mathjax')")
