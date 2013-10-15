import os

c = get_config()
app = c.InteractiveShellApp

load_subconfig('ipython_config.py')

if os.name == 'nt':
    app.exec_lines.append("init_printing(use_latex='mathjax')")
