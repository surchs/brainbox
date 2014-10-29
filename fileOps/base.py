__author__ = 'Sebastian Urchs'
# Imports
import os
import glob


def grab_files(path, ext, sub=None):
    """
    This function pull a couple of files in and also looks in subdirectories
    :param path:
    :param ext:
    :param sub:
    :return:
    """
    # See if there are any subdirectories
    sub_dirs = [d for d in os.walk(path).next()[1]]
    tmp = ext.strip('*')
    ext = '*{}'.format(ext)
    # Create an empty dictionary with three keys for path, dir and name
    out_dict = {key: [] for key in ['sub_name', 'dir', 'path']}
    if sub:
        # We have selected a specific subdirectory to go to
        tmp_dir = os.path.join(path, sub)
        print('I will be pulling files from {}'.format(tmp_dir))
        in_files = glob.glob(os.path.join(tmp_dir, ext))
        for in_file in in_files:
            sub_name = os.path.basename(in_file.split('.')[0])
            if sub_name in out_dict['sub_name']:
                print('Warning: {} from {} is already in the dict!\n'.format(sub, sub_name))
            out_dict['sub_name'].append(sub_name)
            out_dict['dir'].append(sub)
            out_dict['path'].append(in_file)

    elif sub_dirs:
        # There is something in here
        for sub_dir in sub_dirs:
            tmp_dir = os.path.join(path, sub_dir)
            in_files = glob.glob(os.path.join(tmp_dir, ext))
            for in_file in in_files:
                sub_name = os.path.basename(in_file.split('.')[0])
                if sub_name in out_dict['sub_name']:
                    print('Warning: {} from {} is already in the dict!\n'.format(sub_dir, sub_name))
                out_dict['sub_name'].append(sub_name)
                out_dict['dir'].append(sub_dir)
                out_dict['path'].append(in_file)
    else:
        in_files = glob.glob(os.path.join(path, ext))
        for in_file in in_files:
            sub_name = os.path.basename(in_file.split('.')[0])
            if sub_name in out_dict['sub_name']:
                print('Warning: {} from {} is already in the dict!\n'.format(path, sub_name))
            out_dict['sub_name'].append(sub_name)
            out_dict['dir'].append(path)
            out_dict['path'].append(in_file)

    return out_dict