import os
import sys
import matplotlib as mpl
from matplotlib import cm
from colormaps import inferno, magma, plasma, viridis

# Add the notebook dir to the path
if os.name == 'nt':
    nbdir = 'D:/Dropbox/Notebooks'
else:
    nbdir = '~/notebooks'

nbdir = os.path.expanduser(nbdir)
nbdir = os.path.normpath(nbdir)

sys.path.append(nbdir)

# Let's fix jet even before matplotlib 2.0
mpl.cm.cmap_d["inferno"] = inferno
mpl.cm.cmap_d["magma"] = magma
mpl.cm.cmap_d["plasma"] = plasma
mpl.cm.cmap_d["viridis"] = viridis

mpl.cm.inferno = inferno
mpl.cm.magma = magma
mpl.cm.plasma = plasma
mpl.cm.viridis = viridis

mpl.rcParams["image.cmap"] = "viridis"

# Load the default config
load_subconfig('ipython_config.py')

# Set a bunch of stuff to import automatically
c = get_config()
app = c.IPKernelApp

app.matplotlib = 'inline'

app.exec_lines.append('import numpy as np')
app.exec_lines.append('import scipy as sp')
app.exec_lines.append('import pandas as pd')
app.exec_lines.append('import matplotlib as mpl')
app.exec_lines.append('import matplotlib.pyplot as plt')
app.exec_lines.append("nbdir = r'%s'".format(nbdir))

app.exec_lines.append("from sympy import init_printing")

# Setup the SymPy pretty printing
if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='mathjax')")
else:
    app.exec_lines.append("init_printing(use_latex=True)")
