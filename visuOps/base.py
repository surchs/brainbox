__author__ = 'surchs'
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


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

    if titles and len(titles) == 4:
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
    rt = add_subplot_axes(ax, [0.5+dist/2, 0.5+dist/2,
                               0.5-dist/(2-title), 0.5-dist/(2-title)])
    if title:
        rt.set_title(titles[2])
    if not border:
        rt.set_xticks([])
        rt.set_yticks([])
    if not border:
        rt.spines["top"].set_visible(False)
        rt.spines["right"].set_visible(False)
        rt.spines["left"].set_visible(False)
        rt.spines["bottom"].set_visible(False)

    # Make right bottom plot
    rb = add_subplot_axes(ax, [0.5+dist/2, 0,
                               0.5-dist/(2-title), 0.5-dist/(2-title)])
    if title:
        rb.set_title(titles[3])
    if not ticks:
        rb.set_xticks([])
        rb.set_yticks([])
    if not border:
        rb.spines["top"].set_visible(False)
        rb.spines["right"].set_visible(False)
        rb.spines["left"].set_visible(False)
        rb.spines["bottom"].set_visible(False)

    return lt, lb, rt, rb


def make_montage(vol, axis='coronal', x_step=5, y_step=6):
    """
    Makes a montage of a 3D volume
    """
    n_steps = x_step * y_step
    
    if axis == 'coronal':
        it_dim = vol.shape[1]
        x_dim = vol.shape[0]
        y_dim = vol.shape[2]
        
    elif axis == 'axial':
        it_dim = vol.shape[0]
        x_dim = vol.shape[1]
        y_dim = vol.shape[2]

    vis_mat = np.zeros((x_step*x_dim, y_step*y_dim))
    it_slc = np.linspace(0, it_dim-1, n_steps)
    
    itc = 0
    for y in np.arange(y_step):
        for x in np.arange(x_step):
            slc_ind = it_slc[itc]
            get_slc = np.floor(slc_ind)
            if axis == 'coronal':
                slc = vol[:, get_slc, :]
            elif axis == 'axial':
                slc = vol[get_slc, ...]
            vis_mat[x_dim * x : x_dim * (x + 1), y_dim * y : y_dim * (y + 1)] = slc
            itc += 1
    out_mat = np.fliplr(np.rot90(vis_mat))
    return out_mat


def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap