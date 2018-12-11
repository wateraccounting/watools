# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UN-IHE 2018
Contact: t.hessels@un-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/SoilGrids
"""
import os
from watools.Collect.SoilGrids.DataAccess import DownloadData
import sys


def main(Dir, latlim, lonlim, level = 'sl1', Waitbar = 1):
    """
    Downloads SoilGrids data from ftp://ftp.soilgrids.org/data/recent/

    this data includes a Digital Elevation Model (DEM)
    The spatial resolution is 90m (3s) or 450m (15s)

    The following keyword arguments are needed:
    Dir -- 'C:/file/to/path/'
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    level -- 'sl1' (Default) 
             'sl2'     
             'sl3'     
             'sl4'     
             'sl5'     
             'sl6'     
             'sl7'    
    Waitbar -- '1' if you want a waitbar (Default = 1)
    """

    # Create directory if not exists for the output
    output_folder = os.path.join(Dir, 'SoilGrids', 'Clay_Content')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the output map and create this if not exists
    nameEnd = os.path.join(output_folder, 'ClayContentMassFraction_%s_SoilGrids_percentage.tif' %level)

    if not os.path.exists(nameEnd):

        # Create Waitbar
        if Waitbar == 1:
            print('\nDownload Clay Content soil map of %s from SoilGrids.org' %level)
            import watools.Functions.Start.WaitbarConsole as WaitbarConsole
            total_amount = 1
            amount = 0
            WaitbarConsole.printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)

        # Download and process the data
        DownloadData(output_folder, latlim, lonlim, "CLYPPT", level)

        if Waitbar == 1:
            amount = 1
            WaitbarConsole.printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)

    else:
        if Waitbar == 1:
            print("\nClay Content soil map of %s from SoilGrids.org already exists in output folder" %level)
if __name__ == '__main__':
    main(sys.argv)
