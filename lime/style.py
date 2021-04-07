from matplotlib import rc, ticker
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

def subplots(nrows=1, ncols=1, figsize = (4, 3), sharex=True, \
             sharey=True, **kwargs):

    if nrows == 1 and ncols == 1:

        fig, ax = plt.subplots(figsize=figsize, constrained_layout=True, **kwargs)

        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
        ax.tick_params(direction='in', length=6)

        return fig, ax

    elif (nrows > 1 and ncols==1) or (ncols > 1 and nrows==1):

        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex, \
                                sharey=sharey, **kwargs)

        for ax in axs:
            ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
            ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
            ax.tick_params(direction='in', length=6, labelsize=20)


        return fig, axs

    else:

        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, \
                               sharex=True, sharey=True)

        return fig, ax



def set_style(fontsize=12):

    size = fontsize

    #fontProperties = {'family':'sans-serif','sans-serif':['Helvetica'],
    #'weight' : 'normal', 'size' : fontsize}

    fontProperties = {'family':'sans-serif','sans-serif':['Arial'],
    'weight' : 'normal', 'size' : fontsize}

    rc('font', **fontProperties)

    rc('text', usetex=False)

    mpl.rcParams['mathtext.rm'] = 'Computer Modern'
    mpl.rcParams['mathtext.it'] = 'Computer Modern:italic'
    mpl.rcParams['mathtext.bf'] = 'Computer Modern:bold'

    plt.rc('xtick', color='k', labelsize='large', direction='in')
    plt.rc('ytick', color='k', labelsize='large', direction='in')
    plt.rc('xtick.major', size=6, pad=6)
    plt.rc('xtick.minor', size=4, pad=6)
    plt.rc('ytick.major', size=6, pad=6)
    plt.rc('ytick.minor', size=4, pad=6)
    #rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})


#     plt.rcParams['text.latex.preamble'] = [
# ##    r'\usepackage{time}',
#     r'\usepackage{tgheros}',    # helvetica font
#     r'\usepackage[]{amsmath}',   # math-font matching  helvetica
#     r'\usepackage{bm}',
# #    r'\sansmath'                # actually tell tex to use it!
#     r'\usepackage{siunitx}',    # micro symbols
#     r'\sisetup{detect-all}',    # force siunitx to use the fonts
#     ]

    #rc('text.latex', preamble=r'\usepackage{cmbright}')


    plt.rc('axes', titlesize=size)  # fontsize of the axes title
    plt.rc('axes', labelsize=size)  # fontsize of the x any y labels
    # plt.rc('xtick', labelsize=size)  # fontsize of the tick labels
    # plt.rc('ytick', labelsize=size)  # fontsize of the tick labels
    plt.rc('legend', fontsize=size)  # legend fontsize
    plt.rc('figure', titlesize=size)  # # size of the figure title
    plt.rc('axes', linewidth=1)

    #plt.rcParams['axes.labelweight'] = 'normal'

    plt.locator_params(axis='y')

    # the axes attributes need to be set before the call to subplot
    #plt.rc('xtick.major', size=4, pad=4)
    #plt.rc('xtick.minor', size=3, pad=4)
    #plt.rc('ytick.major', size=4, pad=4)
    #plt.rc('ytick.minor', size=3, pad=4)

    plt.rc('savefig',dpi=120)

    plt.legend(frameon=False)

    # matlab rgb line colors
    linecolors = [ (0,    0.4470,    0.7410),
    (0.8500,  0.3250,    0.0980),
    (0.9290,  0.6940,    0.1250),
    (0.4940, 0.1840, 0.5560),
    (0.4660, 0.6740, 0.1880),
    (0.3010, 0.7450, 0.9330),
    (0.6350, 0.0780, 0.1840)]

    plt.rcParams['axes.prop_cycle'] = mpl.cycler(color=linecolors)
    #plt.rcParams["xtick.minor.visible"] =  True


    # using aliases for color, linestyle and linewidth; gray, solid, thick
    #plt.rc('grid', c='0.5', ls='-', lw=5)
    plt.rc('lines', lw=2)
    return

def matplot(x, y, f, vmin=None, vmax=None, output='output.pdf', xlabel='X', \
            ylabel='Y', diverge=False, cmap='viridis', **kwargs):
    """

    Parameters
    ----------
    f : 2D array
        array to be plotted.

    extent: list [xmin, xmax, ymin, ymax]

    Returns
    -------
    Save a fig in the current directory.

    """

    fig, ax = plt.subplots(figsize=(4,3))

    set_style()

    # if diverge:
    #     cmap = "RdBu_r"
    # else:
    #     cmap = 'viridis'

    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)

    extent = [xmin, xmax, ymin, ymax]
    cntr = ax.matshow(f.T, aspect='auto', cmap=cmap, extent=extent, \
                      vmin=vmin, vmax=vmax, **kwargs)

    ax.set_aspect('auto')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.colorbar(cntr)

    ax.xaxis.set_ticks_position('bottom')

#    fig.subplots_adjust(wspace=0, hspace=0, bottom=0.14, left=0.14, top=0.96, right=0.94)

#    fig.savefig(output, dpi=1200)

    return fig, ax

def color_code(x, y, z, fig, ax, cbar=False):
    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(0, 1)
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    # Set the values used for colormapping
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    # if cbar:
    #     cbar = fig.colorbar(line, orientation='horizontal')
    #     cbar.set_ticks([0., 1.])
    #     cbar.set_ticklabels(['matter', 'photon'])

    # ax.set_xlim(-6,4)
    # ax.set_ylim(3.,8.0)

    return line



# if __name__ == '__main__':
#     fig, ax = subplots(ncols=1, nrows=2)
#     import numpy as np
#     x = np.linspace(0,10)
#     ax[1].plot(x, np.sin(x))
