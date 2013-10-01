import os

c = get_config()
load_subconfig('ipython_config.py', profile='default')

lines = """
from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
"""
c.InteractiveShellApp.exec_lines.append(lines)

if os.name == 'nt':
    c.InteractiveShellApp.exec_lines.append("init_printing(use_latex='matplotlib')")
else:
    c.InteractiveShellApp.exec_lines.append("init_printing(use_latex=True)")
