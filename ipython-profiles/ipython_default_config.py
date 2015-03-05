import os

if os.name == "nt":
    os.chdir(r'C:\Users\seanvig2\Documents')

c = get_config()
app = c.InteractiveShellApp

c.IPKernelApp.matplotlib = 'inline'

app.extensions = ['autoreload']
app.exec_lines.append('%autoreload 2')
