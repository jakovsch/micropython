#!/usr/bin/env python

"""
Generate header file with macros defining micro:bit version info.

This script works with Python 2.6, 2.7, 3.3 and 3.4.
"""

from __future__ import print_function

import sys
import os
import datetime
import subprocess

def get_version_info_from_git():
    # Python 2.6 doesn't have check_output, so check for that
    try:
        subprocess.check_output
        subprocess.check_call
    except AttributeError:
        return None

    # Note: git describe doesn't work if no tag is available
    try:
        git_tag = subprocess.check_output(["git", "describe", "--dirty", "--always"], stderr=subprocess.STDOUT, universal_newlines=True).strip()
    except subprocess.CalledProcessError as er:
        if er.returncode == 128:
            # git exit code of 128 means no repository found
            return None
        git_tag = ""
    except OSError:
        return None
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.STDOUT, universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        git_hash = "unknown"
    except OSError:
        return None

    try:
        # Check if there are any modified files.
        subprocess.check_call(["git", "diff", "--no-ext-diff", "--quiet", "--exit-code"], stderr=subprocess.STDOUT)
        # Check if there are any staged files.
        subprocess.check_call(["git", "diff-index", "--cached", "--quiet", "HEAD", "--"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        git_hash += "-dirty"
    except OSError:
        return None

    return git_tag, git_hash

def make_version_header(filename, mpy):
    # Get version info using git, with fallback to docs/conf.py
    info = get_version_info_from_git()
    if info is None:
        info = "unknown", "unknown"

    git_tag, git_hash = info

    # Generate the file with the git and version info
    file_data_ubit = """\
// This file was generated by tools/makeversionhdr.py
#define MICROBIT_GIT_TAG "%s"
#define MICROBIT_GIT_HASH "%s"
#define MICROBIT_BUILD_DATE "%s"
""" % (git_tag, git_hash, datetime.date.today().strftime("%Y-%m-%d"))

    file_data_mpy = """\
// This file was generated by py/makeversionhdr.py
#define MICROPY_GIT_TAG "v1.9.2-%s"
#define MICROPY_GIT_HASH "%s"
#define MICROPY_BUILD_DATE "%s"
#define MICROPY_VERSION_MAJOR (1)
#define MICROPY_VERSION_MINOR (9)
#define MICROPY_VERSION_MICRO (2)
#define MICROPY_VERSION_STRING "1.9.2"
""" % (git_tag, git_hash, datetime.date.today().strftime("%Y-%m-%d"))


    # Check if the file contents changed from last time
    write_file = True
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            existing_data = f.read()
        if mpy == True:
            if existing_data == file_data_mpy:
                write_file = False
        else:
            if existing_data == file_data_ubit:
                write_file = False

    # Only write the file if we need to
    if write_file:
        print("Generate %s" % filename)
        with open(filename, 'w') as f:
            if mpy == True:
                f.write(file_data_mpy)
            else:
                f.write(file_data_ubit)

if __name__ == "__main__":
    make_version_header(sys.argv[1], False)
    make_version_header(sys.argv[2], True)
