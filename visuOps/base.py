__author__ = 'surchs'
from matplotlib import pyplot as plt


def add_subplot_axes(ax, rect, axisbg='w'):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position = ax.transAxes.transform(rect[0:2])
    trans_figure = fig.transFigure.inverted()
    infig_position = trans_figure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]
    subax = fig.add_axes([x, y, width, height], axisbg=axisbg)
    return subax


def add_four_grid(ax, dist=0.05, ticks=False, border=False, titles=None):
    """
    Function that creates a symmetric four grid inside a subplot
    :param ax: Axis handle of parent subplot
    :param dist: Distance between neighbouring fields of the grd
    :param ticks: True if ticks shall be visible
    :param border: True if border shall be visible
    :param titles: Iterable with length 4 in this order:
                    0) top left
                    1) bottom left
                    2) top right
                    3) bottom right
                   If set, distance the fields will be made narrower to
                   accommodate the title
    :return: Axis handles for the four subfields in this order:
                0) top left
                1) bottom left
                2) top right
                3) bottom right
    """
    # See if titles are provided for all subplots
    if len(titles) == 4:
        title = True
    else:
        title = False

    # Make left top plot
    lt = add_subplot_axes(ax, [0, 0.5+dist/2,
                               0.5-dist/(2-title), 0.5-dist/(2-title)])
    if title:
        lt.set_title(titles[0])
    if not ticks:
        lt.set_xticks([])
        lt.set_yticks([])
    if not border:
        lt.spines["top"].set_visible(False)
        lt.spines["right"].set_visible(False)
        lt.spines["left"].set_visible(False)
        lt.spines["bottom"].set_visible(False)

    # Make left bottom plot
    lb = add_subplot_axes(ax, [0, 0,
                               0.5-dist/(2-title), 0.5-dist/(2-title)])
    if title:
        lb.set_title(titles[1])
    if not ticks:
        lb.set_xticks([])
        lb.set_yticks([])
    if not border:
        lb.spines["top"].set_visible(False)
        lb.spines["right"].set_visible(False)
        lb.spines["left"].set_visible(False)
        lb.spines["bottom"].set_visible(False)

    # Make right top plot
    rt = add_subplot_axes(ax, [0.5+dist/2, 0,
                               0.5-dist/(2-title), 0.5-dist/(2-title)])
    if title:
        rt.set_title(titles[0])
    if not border:
        rt.set_xticks([])
        rt.set_yticks([])
    if not border:
        rt.spines["top"].set_visible(False)
        rt.spines["right"].set_visible(False)
        rt.spines["left"].set_visible(False)
        rt.spines["bottom"].set_visible(False)

    # Make right bottom plot
    rb = add_subplot_axes(ax, [0.5+dist/2, 0.5+dist/2,
                               0.5-dist/(2-title), 0.5-dist/(2-title)])
    if title:
        rb.set_title(titles[0])
    if not ticks:
        rb.set_xticks([])
        rb.set_yticks([])
    if not border:
        rb.spines["top"].set_visible(False)
        rb.spines["right"].set_visible(False)
        rb.spines["left"].set_visible(False)
        rb.spines["bottom"].set_visible(False)

    return lt, lb, rt, rb