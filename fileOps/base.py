__author__ = 'Sebastian Urchs'
# Imports
import os
import glob
import numpy as np
import nibabel as nib
from .. import tools as to


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


def read_files(file_dict, network=None):
    """
    :param file_dict: the input dictionary. Should be generated with
                      brainbox.fileOps.grab_files.
    :return: a dictionary with an entry for each subdirectory that was supplied
             in the file_dict. Each entry contains an 4D array with the networks
             ordered in the 4th dimension. If the file read in is 3D, the 4th
             dimension will only have one entry
    """
    array_dict = {}
    num_files = len(file_dict['sub_name'])
    print('I found {} files to load.'.format(num_files))
    count = to.Counter(num_files)
    for idx, sub in enumerate(file_dict['sub_name']):
        # Progress
        count.tic()
        sub_dir = file_dict['dir'][idx]
        sub_path = file_dict['path'][idx]
        try:
            tmp_data = nib.load(sub_path).get_data()
        except:
            count.toc()
            count.progress()
            continue
        if len(tmp_data.shape) > 3:
            n4 = tmp_data.shape[3]
            n3 = tmp_data.shape[:3]
            tmp_flat = np.reshape(tmp_data, (np.prod(n3), n4))
            if network:
                # Get the network out of it
                if network < n4:
                    tmp_flat = tmp_flat[..., network, None]
                else:
                    raise Exception('You requested network {} but the file '
                                    'only has {} networks'.format(network, n4))
        else:
            if network:
                print('You requested network {} but this is a 3D file that '
                      'only has 1 network and I will ignore the request')
            tmp_flat = np.ndarray.flatten(tmp_data)[..., None]

        # See if the metric has been stored yet
        if not sub_dir in array_dict.keys():
            # Find expected number of subjects
            matches = len([s for s in file_dict['sub_name'] if sub_dir in s])
            # Get size of current subject
            sub_size = tmp_flat.shape
            arr_size = (matches,) + sub_size
            # Preallocate array
            array_dict[sub_dir] = [np.empty(arr_size), 0]
        array_dict[sub_dir][0][array_dict[sub_dir][1], ...] = tmp_flat
        array_dict[sub_dir][1] += 1

        # Report on time
        count.toc()
        count.progress()

    # Clean up the arrays - there may be some subjects that did not load etc
    for sub in array_dict.keys():
        tmp_a = array_dict[sub][0]
        tmp_b = array_dict[sub][1]
        array_dict[sub] = tmp_a[:tmp_b, ...]

    print('\nWe are done')
    return array_dict