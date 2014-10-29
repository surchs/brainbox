__author__ = 'surchs'
import numpy as np
import nibabel as nib
from .. import tools as to
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as clh


def read_files(file_dict):
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
        else:
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


def calc_link(data, network, method='euclidean', metric=None):
    """
    Computes the linkage on the data supplied. Uses hierarchical clustering with
    wards criterion
    :param data: The input dictionary (need to find out orientation of the data)
    :param network: (zero-based) index of the desired network
    :param method: the distance method of the scipy spatial distance toolbox
    :param metric: the imaging metric in the dictionary that is desired
    :return: distance and linkage variables
    """

    distance = dist.squareform(dist.pdist(data[metric][..., network], method))
    linkage = clh.linkage(distance, method='ward')

    return distance, linkage