__author__ = 'surchs'
import sys
import time
import numpy as np


class Counter(object):
    """
    Counter Class
    """
    def __init__(self, total=None):
        self.count = 0
        self.total = total
        self.start = time.time()
        self.times = np.array([0])
        self.avg = 0
        self.took = 0
        self.cur_tic = time.time()
        self.cur_toc = time.time()
        self.all = 0

    def tic(self):
        self.cur_tic = time.time()

    def toc(self):
        self.cur_toc = time.time()
        self.count += 1
        self.took = self.cur_toc - self.cur_tic
        self.times = np.append(self.times, self.took)
        self.avg = np.average(self.times)
        self.all = self.cur_toc - self.start

    def progress(self, remaining=None, stepper=None):
        """
        :param remaining:
        :param stepper: if this is something, then don't print a report every
                        time but only on multiples of stepper
        :return:
        """
        if stepper:
            if self.count % stepper == 0:
                self.make_progress(remaining)
            else:
                pass
        else:
            self.make_progress(remaining)

    def make_progress(self, remaining=None):
        if not remaining and not self.total:
            sys.stdout.write('\r {0} done, avg {1:.2f} '
                             'seconds.'.format(self.count,
                                               self.avg))
            return
        elif remaining and not self.total:
            rem_time = self.avg * remaining
            sys.stdout.write('\r {0:.2f} seconds to go. '
                             'One step takes {1:.5f} '
                             'and we ran for {2:.2f} so far'.format(rem_time,
                                                                    self.avg,
                                                                    self.all))
        else:
            remaining = self.total - self.count
            p_complete = float(self.count) / self.total * 100
            rem_time = self.avg * remaining

        sys.stdout.write('\r {0:.1f} % done {1:.2f} seconds to go. '
                         'One step takes {2:.5f} '
                         'and we ran for {3:.2f} so far'.format(p_complete,
                                                                rem_time,
                                                                self.avg,
                                                                self.all))
        sys.stdout.flush()

    def total(self):
        self.cur_toc = time.time()
        self.total = self.cur_toc - self.start
        print('This took a total of {0:.2f} seconds'.format(self.total))