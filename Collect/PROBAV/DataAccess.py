# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UNESCO-IHE 2018
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/PROBAV

Description:
This script collects PROBAV data from the VITO server. The data has a
daily temporal resolution and a spatial resolution of 0.000996 degree. The
resulting tiff files are in the WGS84 projection.
The data is available between 2014-03-11 till present.

Example:
from watools.Collect import PROBAV
PROBAV.5_daily(Dir='C:/Temp/', Startdate='2014-03-11', Enddate='2015-03-11',
                     latlim=[50,54], lonlim=[3,7])

"""
# General modules
import numpy as np
import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import shutil
import gdal
import re
from bs4 import BeautifulSoup

# Water Accounting Modules
import watools.WebAccounts as WebAccounts
import watools.General.data_conversions as DC

def DownloadData(Dir, Startdate, Enddate, latlim, lonlim, Waitbar, type_PROBAV, type_Bands = ['SM','B1','B2','B3','B4']):
    """
    This scripts downloads PROBAV data from the VITO server.
    The output files display the defined bands of PROBA-V.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    lonlim -- [ymin, ymax]
    latlim -- [xmin, xmax]
    """

    # Check the latitude and longitude and otherwise reset lat and lon.
    if latlim[0] < -65 or latlim[1] > 75:
        print('Latitude above 65N or below 75S is not possible.\
            Value set to maximum')
        latlim[0] = np.max(latlim[0], -65)
        latlim[1] = np.min(latlim[1], 75)
    if lonlim[0] < -180 or lonlim[1] > 180:
        print('Longitude must be between 180E and 180W.\
            Now value is set to maximum')
        lonlim[0] = np.max(lonlim[0], -180)
        lonlim[1] = np.min(lonlim[1], 180)

    # Check Startdate and Enddate
    if not Startdate:
        Startdate = pd.Timestamp('2014-03-11')
    if not Enddate:
        Enddate = pd.Timestamp.now()

    # Define some parameters for the different set of PROBA-V Parameters
    if type_PROBAV.split('_')[-1] == "S10":
        type_time = "10-daily"
        Startdate_pandas = pd.Timestamp(Startdate)
        Day = Startdate_pandas.day
        Day_offset = int(np.ceil(((Day -1) / 10. - int(int(Day - 1) / 5)) * 10))  
        Startdate = Startdate_pandas - pd.offsets.Day(Day_offset)
        list_days = [1,11,21]
    elif type_PROBAV.split('_')[-1] == "S5":
        type_time = "5-daily"
        Startdate_pandas = pd.Timestamp(Startdate)
        Day = Startdate_pandas.day
        Day_offset = int(np.ceil(((Day -1) / 5. - int(int(Day - 1) / 5)) * 5)) 
        Startdate = Startdate_pandas - pd.offsets.Day(Day_offset)
        list_days = [1,6,11,16,21,26]
    elif type_PROBAV.split('_')[-1] == "S1":
        type_time = "daily"
        
    # amount of Dates weekly
    Dates = pd.date_range(Startdate, Enddate, freq="D")
    if type_time is not "daily":
        Dates = [date for date in Dates if date.day in list_days]

    # Create Waitbar
    if Waitbar == 1:
        import watools.Functions.Start.WaitbarConsole as WaitbarConsole
        total_amount = len(Dates)
        amount = 0
        WaitbarConsole.printWaitBar(amount, total_amount, prefix='Progress:',
                                    suffix='Complete', length=50)

    # Define directory and create it if not exists
    output_folder = os.path.join(Dir, '%s'%(str(type_PROBAV.split('_')[0])), 'PROBAV', '%s' %type_time)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_folder_temp = os.path.join(Dir, '%s'%(str(type_PROBAV.split('_')[0])), 'PROBAV', '%s' %type_time, 'Temp')
    if not os.path.exists(output_folder_temp):
        os.makedirs(output_folder_temp)

    # loop over dates
    for Date in Dates:

        # Loop over all the required bands
        for type_Band in type_Bands:
        
            # Define end filename
            End_filename = os.path.join(output_folder, '%s_PROBAV_-_%s_%d.%02d.%02d_%s.tif' %(type_PROBAV, type_time, Date.year, Date.month, Date.day, type_Band))
    
            # Download the data from FTP server if the file not exists
            if not os.path.exists(End_filename):
                try:
                    # Download the PROBA-V Data
                    output_files_PROBAV = Download_PROBAV_from_VITO(End_filename,
                                                    output_folder_temp, Date, latlim, lonlim, type_PROBAV, type_Band)

                    # Create dataset
                    Data, Geo_out = Create_Array(output_files_PROBAV, latlim, lonlim)
                    
                    # Save Data
                    DC.Save_as_tiff(End_filename, Data, Geo_out, "WGS84")
    
                except:
                    print("Was not able to create PROBAV file with date %s" % Date)

        # Adjust waitbar
        if Waitbar == 1:
            amount += 1
            WaitbarConsole.printWaitBar(amount, total_amount,
                                        prefix='Progress:', suffix='Complete',
                                        length=50)

    # remove the temporary folder
    #shutil.rmtree(output_folder_temp)
    
    return()


def Download_PROBAV_from_VITO(End_filename, output_folder_temp, Date, latlim, lonlim, type_PROBAV, type_Band):
    """
    This function retrieves PROBAV data for a given date from the
    https://www.vito-eodata.be/PDF/datapool/Free_Data server.

    Restrictions:
    Sign up is needed. The password and username has to be stored within the
    WebAccounts.py

    Keyword arguments
    """

    # Define date
    year_data = Date.year
    month_data = Date.month
    day_data = Date.day

    # Define Tiles
    X_tile_max = int(np.floor((lonlim[1] + 180) / 10.))
    X_tile_min = int(np.floor((lonlim[0] + 180) / 10.))
    Y_tile_min = int(14 - np.ceil((latlim[1] + 65) / 10.))
    Y_tile_max = int(14 - np.ceil((latlim[0] + 65) / 10.))
    X_tiles = list(range(X_tile_min, X_tile_max+1))
    Y_tiles = list(range(Y_tile_min, Y_tile_max+1))
    output_files_PROBAV = []
    
    # Band numbers PROBA-V
    Band_numbers = {'SM':7,'B1':8,'B2':10,'B3':9,'B4':11}
 
    # Get passwords
    username, password = WebAccounts.Accounts(Type='VITO')
    
    # Download all the needed tiles
    for X_tile in X_tiles:
        for Y_tile in Y_tiles:
    
            # filename of ASCAT data on server
            PROBAV_date = "%d%02d%02d" % (year_data, month_data, day_data)
            URL_name = "https://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/%s_%s_100_m_C1/%s/%s/%s/" %(type_PROBAV.split('_')[-1], type_PROBAV.split('_')[0], year_data, month_data, day_data)
        
            # Get version name
            f = requests.get(URL_name,auth = (username, password))
            x = f.content
            soup = BeautifulSoup(x, "lxml")
            i = str(soup.findAll('a', attrs = {'href': re.compile('(?i)(V10\d)')})[0])
            match = re.search(r'_V10\w+', i)
            PROBAV_Version = match.group()

            # Define some output names
            PROBAV_filename = "PROBAV_%s_%s_X%02dY%02d_%s_100M%s.HDF5" %(type_PROBAV.split('_')[-1], type_PROBAV.split('_')[0], X_tile, Y_tile, PROBAV_date, PROBAV_Version)
            PROBAV_name = 'PV_%s_%s-%s_100M%s' %(type_PROBAV.split('_')[-1], type_PROBAV.split('_')[0], PROBAV_date, PROBAV_Version)
            PROBAV_filename_tiff = os.path.join(output_folder_temp, "PROBAV_%s_%s_X%02dY%02d_%s_100M%s_%s.tif" %(type_PROBAV.split('_')[-1], type_PROBAV.split('_')[0], X_tile, Y_tile, PROBAV_date, PROBAV_Version, type_Band))
             
            # Output 
            output_file_PROBAV = os.path.join(output_folder_temp, PROBAV_filename)
            if not os.path.exists(PROBAV_filename_tiff):
                if not os.path.exists(output_file_PROBAV):
                    URL = "https://www.vito-eodata.be/PDF/datapool/Free_Data/PROBA-V_100m/%s_%s_100_m_C1/%s/%s/%s/%s/%s" % (type_PROBAV.split('_')[-1], type_PROBAV.split('_')[0], year_data, month_data, day_data,
                                                          PROBAV_name, PROBAV_filename)
                    # Download the ASCAT data
                    try:
                        y = requests.get(URL, auth=HTTPBasicAuth(username, password))
                    except:
                        from requests.packages.urllib3.exceptions import InsecureRequestWarning
                        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                
                        y = requests.get(URL, auth=(username, password), verify=False)
                    
                    # Write the file in system
                    try:                        
                        z = open(output_file_PROBAV, 'wb')
                        z.write(y.content)
                        z.close()
                    except:
                        print("%s is not available" %output_file_PROBAV)
                    
                # Convert hdf5 into tiff    
                try:
                    # output PROBA-V tiff
                    Band_number = Band_numbers[type_Band]
                    if not type_Band == "SM":
                        scaling_factor = 0.005
                    else:
                        scaling_factor = 1.0  
                    
                    # Define the x and y spacing
                    g = gdal.Open(output_file_PROBAV, gdal.GA_ReadOnly)
                    Meta_data = g.GetMetadata()
                    Lat_Top = float(Meta_data['LEVEL3_GEOMETRY_TOP_RIGHT_LATITUDE'])
                    Lon_Left = float(Meta_data['LEVEL3_GEOMETRY_BOTTOM_LEFT_LONGITUDE'])
                    Pixel_size = float((Meta_data['LEVEL3_RADIOMETRY_BLUE_TOC_MAPPING']).split(' ')[-3]) 
                    
                    # Define the georeference of the HDF5 file
                    geo_out = [Lon_Left-0.5*Pixel_size, Pixel_size, 0, Lat_Top+0.5*Pixel_size, 0, -Pixel_size] 
        
                    # Convert hdf5 to tiff
                    DC.Convert_hdf5_to_tiff(output_file_PROBAV, PROBAV_filename_tiff, Band_number, scaling_factor, geo_out)
                  
                    # Define all the good outputs
                    output_files_PROBAV = np.append(output_files_PROBAV, PROBAV_filename_tiff)
                    
                except:
                    print("%s is not created, and replaced by fake dataset" %PROBAV_filename_tiff)
 
                    # Create empty dataset with nan values
                    Empty_Data = np.ones([10080, 10080]) * np.nan
                    Size_Pixel_PROBAV = 0.000992063492063
                    x_min = X_tile * 10 - 0.5 * Size_Pixel_PROBAV - 180
                    y_max =  Y_tile * -10 + 0.5 * Size_Pixel_PROBAV + 75      
                    Geo_out_fake = tuple([x_min, Size_Pixel_PROBAV, 0, y_max, 0, -Size_Pixel_PROBAV])
                    
                    # Save the fake layer
                    DC.Save_as_tiff(PROBAV_filename_tiff, Empty_Data, Geo_out_fake, "WGS84")
                    
            else:
                # Define all the good outputs
                output_files_PROBAV = np.append(output_files_PROBAV, PROBAV_filename_tiff)
                                  
    return(output_files_PROBAV)

def Create_Array(output_files_PROBAV, latlim, lonlim):
    
    # Define the starting values for lat and lon
    x_uniques = []
    y_uniques = []  
    x_min = [180]
    y_max = [-90]    
    
    # Loop over the output file of PROBA-V to define the extent
    for output_file_PROBAV in output_files_PROBAV:
        dest = gdal.Open(output_file_PROBAV)
        geo_one = dest.GetGeoTransform()
        size_x = dest.RasterXSize
        size_y = dest.RasterYSize
        
        # Define the latitude and longitude per pixel
        xs = np.arange(0,size_x) * geo_one[1] + geo_one[0]
        ys = np.arange(0,size_y) * geo_one[5] + geo_one[3]    
        
        # Define the right pixels within the area
        xs_bool = [np.logical_and(xs > lonlim[0], xs < lonlim[1])][0]
        ys_bool = [np.logical_and(ys > latlim[0], ys < latlim[1])][0]

        # Define the min and max pixels within the area
        x_min = np.minimum(x_min, np.min(xs[xs_bool]))
        y_max = np.maximum(y_max, np.max(ys[ys_bool]))
        
        # Add the latitude and longitude in the end pixels
        x_uniques = np.unique(np.append(x_uniques, xs[xs_bool]))
        y_uniques = np.unique(np.append(y_uniques, ys[ys_bool]))   
       
    # Create end dataset    
    Data = np.ones([len(y_uniques), len(x_uniques)]) * np.nan  
    
    # Loop over input files to fill in the end dataset
    for output_file_PROBAV in output_files_PROBAV:
        
        # Open dataset
        dest = gdal.Open(output_file_PROBAV)
        geo_one = dest.GetGeoTransform()
        
        # Define area
        xs = np.arange(0,size_x) * geo_one[1] + geo_one[0]
        ys = np.arange(0,size_y) * geo_one[5] + geo_one[3]    
        xs_bool = [np.logical_and(xs >= lonlim[0], xs <= lonlim[1])][0]
        ys_bool = [np.logical_and(ys >= latlim[0], ys <= latlim[1])][0]
        yxs_bool = xs_bool * ys_bool[:, None]   
        
        # Define area for end dataset
        xs_end = np.sort(x_uniques)
        ys_end = np.flipud(np.sort(y_uniques)) 
        xs_bool_end = [np.logical_and(xs_end >= np.maximum(lonlim[0],xs[0]), xs_end <= np.minimum(lonlim[1],xs[-1]))][0]
        ys_bool_end = [np.logical_and(ys_end >= np.maximum(latlim[0],ys[-1]), ys_end <= np.minimum(latlim[1],ys[0]))][0]
        yxs_bool_end = xs_bool_end * ys_bool_end[:, None] 
        
        # Open dataset 
        Array_one = dest.GetRasterBand(1).ReadAsArray()
        
        # Add dataset to end dataset
        Data[np.where(yxs_bool_end==True)] = Array_one[np.where(yxs_bool==True)]
        
        # remove the dest
        dest = None
        
    # Create end geo transform    
    Geo_out = tuple([x_min[0], geo_one[1], 0, y_max[0], 0, geo_one[5]])    
    
    return(Data, Geo_out)