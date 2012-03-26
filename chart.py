# chart.py
# Create heatmap from results
# Usage: chart.py [name of csv file]

# !/usr/bin/python

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


import math
import sys

import util


def main(filename):    
    plotname = filename[:filename.find('.')] # remove ".csv"

    x, y, ids = util.process_csv_list(filename)
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=(10, 4))
    heatmap = heatmap[::-1]
    
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap, extent=extent, interpolation='nearest')
    plt.colorbar()
    plt.savefig(plotname)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
