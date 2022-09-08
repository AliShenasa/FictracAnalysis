### Functions to process fictrac data

import pandas as pd
import numpy as np

def loadFictracDat(datfile, withScanInfo=False):
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
    if (withScanInfo):
        colNames.append('scanvolts')
    
    ficDat = pd.read_csv(datfile, names=colNames, header=None)
    return ficDat

def isScanning(volts):
    """
    Given a voltage return true if it is above the threshold for scanning
    Assumes a threshold of 2.5 mv ?(not sure about the units)
    """
    threshold = 2.5
    return volts > threshold

def getPartialScanPeriods(ficDat, length=None):
    """
    Given a dataframe of fictrac data with scan info
    Return list of scan periods
    Used as input to getFullScanPeriods in order to get the full scan periods
    """

    if length is None: # Set length to process as entire range if none given
        length = len(ficDat)
    
    scanArray = np.empty(0)
    prevState = isScanning(ficDat.iloc[0]['scanvolts'])
    startFrame = ficDat.iloc[0]['cnt']

    for i in range(length):
        curState = isScanning(ficDat.iloc[i]['scanvolts'])
        
        if (curState != prevState):
            curFrame = ficDat.iloc[i]['cnt']
            frameLength = curFrame - startFrame
            scanArray = np.append(scanArray, {'frameStart':startFrame, 
                                              'frameEnd':curFrame,
                                              'frameLength':frameLength,
                                              'isScanning':prevState} )
            startFrame = curFrame
        prevState = curState

    return scanArray

def getFullScanPeriods(scanArray):
    """
    Given a list of partial scan periods
    Return a list of full scan periods 
    A full scan is a group of 3 partial scans, groups are seperated by longer breaks
    To find a group match for a long break then 2 short breaks
    The start is at the end frame of the long break
    And the end is at the end frame of the partial scan after the last short break
    """

    breakThreshold = 20.5 #midpoint between short and long scan breaks (14 and 27)

    fullScans = np.empty(0)

    i = 0 # index of array
    while (i+5 < len(scanArray)):
        # Assumes scanning and breaks alternate in scanArray
        if (scanArray[i]['isScanning'] == True):
            i += 1 # Shift index to not scanning frames
        
        if (scanArray[i]['isScanning'] == False):
            if (scanArray[i]['frameLength'] > breakThreshold and 
                scanArray[i+2]['frameLength'] < breakThreshold and 
                scanArray[i+4]['frameLength'] < breakThreshold): # Matches a long short short break pattern
                print(f"full scan from frame {scanArray[i]['frameEnd']} to frame {scanArray[i+5]['frameEnd']}")
                fullScans = np.append(fullScans, {'frameStart': scanArray[i]['frameEnd'],
                                                'frameEnd': scanArray[i+5]['frameEnd'],
                                                'frameLength': scanArray[i+5]['frameEnd'] - scanArray[i]['frameEnd']})

        i += 2 ## Move to next scan break
    return fullScans

def findScanPeriod(fullScans, frame):
    """
    Given a list of full scan periods
    Return a list with the scan that the frame falls into
    If the frame falls outside of a scan, return the 2 adjacent scans
    """

    prevScan = {'frameStart': 0,
                'frameEnd': 0,
                'frameLength': 0}
    for scan in fullScans:
        if scan['frameStart'] < frame and scan['frameEnd'] > frame:
            return [scan]
        
        elif prevScan['frameEnd'] < frame and scan['frameStart'] > frame:
            return [prevScan, scan]

        prevScan = scan

def getScanData(scanList, ficDat):
    """
    Given a sequential list of scan periods
    Return the section of the fictrac dataframe that contains the scans
    """

    startFrame = int(scanList[0]['frameStart'])
    endFrame = int(scanList[-1]['frameEnd'])

    return ficDat.loc[ficDat['cnt'].isin(range(startFrame, endFrame+1))]