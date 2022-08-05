from venv import create
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import pandas as pd
import argparse


def createPanel(x, y, width, height, figureWidth, figureHeight):
    """
    Creates a panel
    width, and height are normalized to the figure's width and height
    """
    return plt.axes([x, y ,width/figureWidth, height/figureHeight])

def loadFictracDat(datfile):
    """Given a fictrac .dat file, return a dataframe of the data"""
    colNames = ['cnt', 
                'dr_cam_x', 'dr_cam_y', 'dr_cam_z', 'dr_cam_err',
                'dr_lab_x', 'dr_lab_y', 'dr_lab_z',
                'r_cam_x', 'r_cam_y', 'r_cam_z',
                'r_lab_x', 'r_lab_y', 'r_lab_z',
                'posx', 'posy', 'heading',
                'step_dir', 'step_mag',
                'intx', 'inty',
                'ts', 'seq', 'dts', 'ms']
    ficDat = pd.read_csv(datfile, names=colNames, header=None)
    return ficDat

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

    # Create figure and panel
    figureWidth=7
    figureHeight=3

    fig, axs = plt.subplots(1, 3, figsize=(figureWidth, figureHeight), constrained_layout=True, sharex='row', sharey='row')

    # Parse fictrac data file
    ficDat = loadFictracDat(infile)

    axs[0].plot(ficDat['inty'], ficDat['intx'])
    axs[0].set_title('integrated forward/side\nmotion')

    axs[1].plot(ficDat['r_cam_y'], ficDat['r_cam_x'])
    axs[1].set_title('absolute rotation\nvector (cam)')

    axs[2].plot(ficDat['posy'], ficDat['posx'])
    axs[2].set_title('integrated x/y\nposition (lab)')



    # view = 'r_cam'

    # for index, pos in enumerate(['x', 'y', 'z']):
    #     axs[0,index].plot(ficDat['d' + view + '_' + pos])

    # for index, pos in enumerate(['x', 'y', 'z']):
    #     axs[1,index].plot(ficDat[view + '_' + pos])

    # for index, pos in enumerate([('y','x'), ('y', 'z'), ('x','z')]):
    #     axs[2,index].plot(ficDat[view + '_' + pos[0]], ficDat[view + '_' + pos[1]])
    #     axs[2,index].set_title('rot {} vs rot {}'.format(pos[0], pos[1]))


    plt.savefig(outfile, dpi=600)

if __name__ == "__main__":
    main()