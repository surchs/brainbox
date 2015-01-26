__author__ = 'surchs'
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as clh


def calc_link(data, metric, method='euclidean', network=0):
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


def scores(data, part):
    """
    Python adaptation of the scores method that was first coded in matlab
    :data: number of features by number of some other thing
    :part: the partition containing target and such
    :return:
    """
    pass
