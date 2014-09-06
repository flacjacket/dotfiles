#!/usr/bin/env python
import os
import shutil
from distutils.util import strtobool

home = os.path.expanduser("~")
dotfiles_dir = os.path.dirname(os.path.abspath(__file__))
dotfiles_dir = os.path.join(dotfiles_dir, "dotfiles")
dotfiles = os.listdir(dotfiles_dir)

for dotfile in dotfiles:
    fp = os.path.join(home, "." + dotfile)
    dotfile = os.path.join(dotfiles_dir, dotfile)
    if os.path.exists(fp) or os.path.islink(fp):
        overwrite = input("%s exists, overwrite? [y/N] " % fp) or "n"
        try:
            overwrite = strtobool(overwrite)
        except ValueError:
            print("Unknown response, skipping")
            continue
        if overwrite:
            if os.path.isfile(fp) or os.path.islink(fp):
                try:
                    os.remove(fp)
                except OSError:
                    print("Failed to remove %s" % fp)
                    continue
            else:
                try:
                    shutil.rmtree(fp)
                except OSError:
                    print("Failed to remove %s" % fp)
                    continue
        else:
            continue
    print("Creating %s" % fp)
    try:
        os.symlink(dotfile, fp)
    except OSError:
        print("Failed to create symlink")
