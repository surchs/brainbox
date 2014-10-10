__author__ = 'sebastian'
import sys
import time
import scipy.io as si


def load_label(in_path):
    f = open(in_path, 'rb')
    lines = f.readlines()
    uselines = []
    for line in lines:
        useline = line.strip()
        uselines.append(useline)
    f.close()

    return uselines


def load_matrix(in_path):
    in_data = si.loadmat(in_path)
    data = in_data['in_array']
    return data


def list_to_str(in_list):
    out_str = ''
    for item in in_list:
        out_str += item + ','
    out_str.strip(',')
    return out_str


def write_line(in_line):
    loop_count = len(in_line)
    out_str = ''
    for num in xrange(loop_count):
        out_str += repr(in_line[num]) + ','
    out_str = out_str.strip(',')
    return out_str


def Main(in_array_path, row_header_path, col_header_path, out_path, start):
    row_hd = load_label(row_header_path)
    col_hd = load_label(col_header_path)
    array = load_matrix(in_array_path)
    out_str = ',' + list_to_str(col_hd) + '\n'
    for id, sub in enumerate(row_hd):
        out_str += sub + ',' + write_line(array[id,:]) + '\n'

    f = open(out_path, 'wb')
    f.write(out_str)
    f.close()
    stop = time.time()
    elapsed = stop - start
    print('\n\nDone! This took me %.4f seconds.' % elapsed)
    print('Wrote the output at %s.\nGoodbye\n\n' % out_path)


if __name__ == '__main__':
    start = time.time()
    if len(sys.argv) < 5:
        message = ('Hey, I can\'t handle your inputs. I am looking for this:\n'
                   + '\npython dump_to_csv.py\n'
                   + '    /path/to/aray.mat\n'
                   + '    /path/to/row_header.txt\n'
                   + '    /path/to/column_header.txt\n'
                   + '    /path/to/output.csv\n'
                   + '\nAll in one line.')
        print(message)
        pass
    else:
        in_array_path = sys.argv[1]
        row_header_path = sys.argv[2]
        col_header_path = sys.argv[3]
        out_path = sys.argv[4]
        Main(in_array_path, row_header_path, col_header_path, out_path, start)
