#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Wrapper for existing code"""

import re
import sys
import utilities

def main(path_to_images, path_to_labels):
    __launch_mma_nb(path_to_images + "\n" + path_to_labels)
    pass

if __name__ == '__main__':
    args = sys.argv
    if (len(args) == 3):
        main(args[1], args[2])
    else:
        print("Need two arguments: path to images, path to labels")