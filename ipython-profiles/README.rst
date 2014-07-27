IPython Profiles
================

Here are the IPython profiles I have setup.  The files are such that
`ipython_profilename_config.py` is linked to
`~/.ipython/profile_profilename/ipython_config.py`. The `nbserver` profile uses
`nbserver_custom.js`, which is linked to
`~/.ipython/profile_nbserver/static/custom/custom.js`.  In addition,
`extensions` and `nbextensions` are linked into the `~/.ipython/` directory.
These profiles are designed to work well on both Linux (which I use on personal
computers) and Windows (which I use on my lab computer), and some things are
hard-coded to reflect these two uses.  The profiles I have setup are:

default
-------

Load the `autoreload` magic.

sympy
-----

Load the SymPy module and define the standard set of symbolic variables for
SymPy.  Initialize the IPython printing of SymPy objects.

labwork
-------

Load modules I use regularly when doing lab work, including numpy, scipy,
pandas, and matplotlib, and loading the `sympy` profile.

nbserver
--------

Profile for launching persistent notebook server.  This will load the `labwork`
profile and do some basic configuration to the notebook environment.
