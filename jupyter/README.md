# Jupyter Config Files

Here are my configuration files for Jupyter and the Jupyter notebook.  These
files and directories are located in:

`jupyter_notebook_config.py` > `~/.jupyter`

`nbconfig` > `~/.jupyter`

`nbextensions` > `~/.local/share/jupyter`

# IPython Profiles

Since Jupyter came along, a lot of the configuration happens there, these
configuration files just get stuff loaded into my namespace nicely.  Using
Jupyter, only the default profile matters, so both `ipython_config.py` and
`ipython_kernel_config.py` should go in `~/.ipython/profile_default/`. The
former just starts up the autoreload plugin for vanilla IPython, while the
later imports a lot of stuff for the notebook.
