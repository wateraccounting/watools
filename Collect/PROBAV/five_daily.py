# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 07:54:17 2017

@author: tih
"""
import sys
from watools.Collect.PROBAV.DataAccess import DownloadData


def main(Dir, Startdate='', Enddate='', latlim=[-65, 75],
         lonlim=[-180, 180], Waitbar=1, type_PROBAV = 'TOC_S5', type_Bands = ['SM', 'B1', 'B2', 'B3', 'B4']):
    """
    This function downloads 5 daily PROBA-V data

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    latlim -- [ymin, ymax] (values must be between -60 and 70)
    lonlim -- [xmin, xmax] (values must be between -180 and 180)
    """
    print('\nDownload 5 daily PROBA-V TOC data for the period %s till %s'\
        % (Startdate, Enddate))

    # Download data
    DownloadData(Dir, Startdate, Enddate, latlim, lonlim, Waitbar, type_PROBAV = 'TOC_S5', type_Bands = ['SM','B1','B2', 'B3','B4'])

if __name__ == '__main__':
    main(sys.argv)
