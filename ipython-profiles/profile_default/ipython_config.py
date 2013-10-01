import os
if os.name == "nt":
    os.chdir('C:\\Users\\seanvig2\\Documents')

c = get_config()
c.InteractiveShellApp.extensions = ['autoreload']

c.InteractiveShellApp.exec_lines = []
c.InteractiveShellApp.exec_lines.append('%autoreload 2')
