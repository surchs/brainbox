__author__ = 'surchs'
import sys
import time
import numpy as np
import nibabel as nib


def read_files(file_dict, network):
    array_dict = {}
    drop = 0
    num_files = len(file_dict['sub_name'])
    print('I found {} files to load.'.format(num_files))
    t_time = np.array([])
    for idx, sub in enumerate(file_dict['sub_name']):
        # Progress
        start = time.time()
        p_complete = np.round(float(idx + 1) / num_files * 100, 1)
        remaining = num_files - (idx + 1)

        sub_dir = file_dict['dir'][idx]
        sub_path = file_dict['path'][idx]
        try:
            tmp_data = nib.load(sub_path).get_data()
        except:
            drop += 1
            continue
        if len(tmp_data.shape) > 3:
            tmp_net = tmp_data[..., network]
        else:
            tmp_net = tmp_data
        tmp_flat = np.ndarray.flatten(tmp_net)
        # See if the metric has been stored yet
        if not sub_dir in array_dict.keys():
            array_dict[sub_dir] = tmp_flat[:, None]
        else:
            array_dict[sub_dir] = np.concatenate((array_dict[sub_dir],
                                                  tmp_flat[:, None]), axis=1)

        # Report on time
        stop = time.time()
        took = stop - start
        t_time = np.append(t_time, took)
        avg_took = np.average(t_time)
        rem_time = np.round((avg_took * remaining), 2)
        # Progress callout
        sys.stdout.write('\r{1} % done {2} seconds to go'.format(p_complete,
                                                                 rem_time))
        sys.stdout.flush()

    print('I had to drop {} files.'.format(drop))