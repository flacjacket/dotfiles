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

app.exec_lines.append('import numpy as np')
app.exec_lines.append('import scipy as sp')
app.exec_lines.append('import pandas as pd')
app.exec_lines.append('import matplotlib.pyplot as plt')
app.exec_lines.append('from curve_fitting import *')
app.exec_lines.append('from spec import *')

if os.name == 'nt':
    c.IPythonWidget.font_family = 'DejaVu Sans Mono'
