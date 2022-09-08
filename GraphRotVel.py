import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import pandas as pd
import argparse
import fictrac_processing as fictrac


def createPanel(x, y, width, height, figureWidth, figureHeight):
    """
    Creates a panel
    width, and height are normalized to the figure's width and height
    """
    return plt.axes([x, y ,width/figureWidth, height/figureHeight])

def getStripAngle(curtime):
    """Assumes angle of fly stripes based on time since start of script"""
    pass

def main():

    # Setup argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile','-i', type=str, action='store', help='input file')
    parser.add_argument('--outfile','-o', type=str, action='store', help='output file')
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    # Create figure and subplot panels
    figureWidth=7
    figureHeight=7

    fig, axs = plt.subplots(3, 3, figsize=(figureWidth, figureHeight), constrained_layout=True, sharex='row', sharey='row')

    # Parse fictrac data file
    ficDat = fictrac.loadFictracDat(infile)

    view = 'r_cam'

    for index, pos in enumerate(['x', 'y', 'z']):
        axs[0,index].plot(ficDat['d' + view + '_' + pos])

    for index, pos in enumerate(['x', 'y', 'z']):
        axs[1,index].plot(ficDat[view + '_' + pos])

    for index, pos in enumerate([('y','x'), ('y', 'z'), ('x','z')]):
        axs[2,index].plot(ficDat[view + '_' + pos[0]], ficDat[view + '_' + pos[1]])
        axs[2,index].set_title('rot {} vs rot {}'.format(pos[0], pos[1]))


    plt.savefig(outfile, dpi=600)

if __name__ == "__main__":
    main()