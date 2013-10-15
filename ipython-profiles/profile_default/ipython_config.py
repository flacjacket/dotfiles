import os
if os.name == "nt":
    os.chdir('C:\\Users\\seanvig2\\Documents')

c = get_config()
app = c.InteractiveShellApp

app.extensions = ['autoreload']

app.exec_lines = []
app.exec_lines.append('%autoreload 2')
app.exec_lines.append('import numpy as np')
app.exec_lines.append('import scipy as sp')
app.exec_lines.append('import pandas as pd')
app.exec_lines.append('import matplotlib.pyplot as plt')
