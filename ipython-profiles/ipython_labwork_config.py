import os

c = get_config()
app = c.InteractiveShellApp

load_subconfig('ipython_config.py', profile='sympy')

app.exec_lines.append('import numpy as np')
app.exec_lines.append('import scipy as sp')
app.exec_lines.append('import pandas as pd')
app.exec_lines.append('import matplotlib.pyplot as plt')

if os.name == 'nt':
    c.IPythonWidget.font_family = 'DejaVu Sans Mono'
