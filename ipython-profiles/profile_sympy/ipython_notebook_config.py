import os

c = get_config()
load_subconfig('ipython_config.py')

if os.name == 'nt':
    c.InteractiveShellApp.exec_lines.append("init_printing(use_latex='mathjax')")
