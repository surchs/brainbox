__author__ = 'surchs'
# Imports
import os
import re
import glob


def grab_files(path, string, ext):
    # See if there are any subdirectories
    sub_dirs = [d for d in os.walk(path).next()[1]]
    dict_files = {}
    if sub_dirs:
        # There is something in here
        for sub_dir in sub_dirs:
            tmp_dir = os.path.join(path, sub_dir)
            in_files = glob.glob(os.path.join(tmp_dir, string, ext))
            for in_file in in_files:
                sub_name = os.path.basename(os.path.splitext(in_file)[0])
                if sub_name in dict_files.keys():
                    print('Warning: {} from {} is already in the dict!\n'.format(sub_dir, sub_name))
                dict_files[sub_name] = in_file
    else:
        in_files = glob.glob(os.path.join(path, string, ext))
        for in_file in in_files:
            sub_name = os.path.basename(os.path.splitext(in_file)[0])
            if sub_name in dict_files.keys():
                print('Warning: {} from {} is already in the dict!\n'.format(path, sub_name))
            dict_files[sub_name] = in_file

    return dict_files