__author__ = 'surchs'
import os
import numpy as np
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as clh

eucl = squareform(pdist(feat_array.T, 'euclidean'))