import os

c = get_config()
app = c.InteractiveShellApp

lines = """\
from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
"""
app.exec_lines.append(lines)

if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='matplotlib')")
else:
    app.exec_lines.append("init_printing(use_latex=True)")
