# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UNESCO-IHE 2019
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/GPM
"""

import numpy as np
import os
import pandas as pd
import requests
import calendar
from joblib import Parallel, delayed

import watools.General.data_conversions as DC

def DownloadData(Dir, Startdate, Enddate, latlim, lonlim, Waitbar, cores, TimeCase):
    """
    This function downloads TRMM daily or monthly data

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    latlim -- [ymin, ymax] (values must be between -60 and 60)
    lonlim -- [xmin, xmax] (values must be between -180 and 180)
    cores -- The number of cores used to run the routine. It can be 'False'
             to avoid using parallel computing routines.
    TimeCase -- String equal to 'daily' or 'monthly'
    Waitbar -- 1 (Default) will print a waitbar
    """
    # String Parameters
    if TimeCase == 'daily':
        TimeFreq = 'D'
        output_folder = os.path.join(Dir, 'Precipitation', 'GPM', 'Daily')
    elif TimeCase == 'monthly':
        TimeFreq = 'MS'
        output_folder = os.path.join(Dir, 'Precipitation', 'GPM', 'Monthly')
    else:
        raise KeyError("The input time interval is not supported")

	# Make directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

	# Check variables
    if not Startdate:
        Startdate = pd.Timestamp('2014-04-01')
    if not Enddate:
        Enddate = pd.Timestamp('Now')
    Dates = pd.date_range(Startdate,  Enddate, freq=TimeFreq)

    # Create Waitbar
    if Waitbar == 1:
        import watools.Functions.Start.WaitbarConsole as WaitbarConsole
        total_amount = len(Dates)
        amount = 0
        WaitbarConsole.printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)

    if latlim[0] < -90 or latlim[1] > 90:
        print('Latitude above 90N or below 90S is not possible.'
               ' Value set to maximum')
        latlim[0] = np.max(latlim[0], -90)
        latlim[1] = np.min(lonlim[1], 90)
    if lonlim[0] < -180 or lonlim[1] > 180:
        print('Longitude must be between 180E and 180W.'
               ' Now value is set to maximum')
        lonlim[0] = np.max(latlim[0], -180)
        lonlim[1] = np.min(lonlim[1], 180)

    # Define IDs
    yID = np.int16(np.array([np.ceil((latlim[0] + 90)*10),
                                   np.floor((latlim[1] + 90)*10)]))
    xID = np.int16(np.array([np.floor((lonlim[0])*10),
                             np.ceil((lonlim[1])*10)]) + 1800)

    # Pass variables to parallel function and run
    args = [output_folder, TimeCase, xID, yID, lonlim, latlim]

    if not cores:
        for Date in Dates:
            RetrieveData(Date, args)
            if Waitbar == 1:
                amount += 1
                WaitbarConsole.printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)
        results = True
    else:
        results = Parallel(n_jobs=cores)(delayed(RetrieveData)(Date, args)
                                         for Date in Dates)

    return results


def RetrieveData(Date, args):
    """
    This function retrieves TRMM data for a given date from the
    ftp://disc2.nascom.nasa.gov server.

    Keyword arguments:
    Date -- 'yyyy-mm-dd'
    args -- A list of parameters defined in the DownloadData function.
    """
    # Argument
    [output_folder, TimeCase, xID, yID, lonlim, latlim] = args

    year = Date.year
    month= Date.month
    day = Date.day

    from watools import WebAccounts
    username, password = WebAccounts.Accounts(Type = 'NASA')

    # Create https
    if TimeCase == 'daily':
        URL = 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGDF.05/%d/%02d/3B-DAY.MS.MRG.3IMERG.%d%02d%02d-S000000-E235959.V05.nc4.ascii?precipitationCal[%d:1:%d][%d:1:%d]'  %(year, month, year, month, day, xID[0], xID[1]-1, yID[0], yID[1]-1)
        DirFile = os.path.join(output_folder, "P_TRMM3B42.V7_mm-day-1_daily_%d.%02d.%02d.tif" %(year, month, day))
        Scaling = 1

    if TimeCase == 'monthly':
        URL = 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/hyrax/GPM_L3/GPM_3IMERGM.05/%d/3B-MO.MS.MRG.3IMERG.%d%02d01-S000000-E235959.%02d.V05B.HDF5.ascii?precipitation[%d:1:%d][%d:1:%d]'  %(year, year, month, month, xID[0], xID[1]-1, yID[0], yID[1]-1)
        Scaling = calendar.monthrange(year,month)[1] * 24
        DirFile = os.path.join(output_folder, "P_GPM.IMERG_mm-month-1_monthly_%d.%02d.01.tif" %(year, month))

    if not os.path.isfile(DirFile):
        dataset = requests.get(URL, allow_redirects=False,stream = True)
        try:
            get_dataset = requests.get(dataset.headers['location'], auth = (username,password),stream = True)
        except:
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            get_dataset  = requests.get(dataset.headers['location'], auth = (username, password), verify = False)

        # download data (first save as text file)
        pathtext = os.path.join(output_folder,'temp.txt')
        z = open(pathtext,'wb')
        z.write(get_dataset.content)
        z.close()

        # Open text file and remove header and footer
        data_start = np.genfromtxt(pathtext,dtype = float,skip_header = 1,delimiter=',')
        data = data_start[:,1:] * Scaling
        data[data < 0] = -9999
        data = data.transpose()
        data = np.flipud(data)

        # Delete .txt file
        os.remove(pathtext)

        # Make geotiff file
        geo = [lonlim[0], 0.1, 0, latlim[1], 0, -0.1]
        DC.Save_as_tiff(name=DirFile, data=data, geo=geo, projection="WGS84")

    return True
