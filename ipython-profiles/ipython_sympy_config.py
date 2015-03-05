import os

c = get_config()
app = c.InteractiveShellApp

lines = """\
import sympy as sym
x, y, z, t = sym.symbols('x y z t')
k, m, n = sym.symbols('k m n', integer=True)
f, g, h = sym.symbols('f g h', cls=Function)
"""
app.exec_lines.append(lines)

if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='matplotlib')")
else:
    app.exec_lines.append("init_printing(use_latex=True)")
