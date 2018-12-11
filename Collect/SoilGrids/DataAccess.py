# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UNESCO-IHE 2016
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/DEM
"""

# General modules
import os
import shutil
from ftplib import FTP

# WA+ modules
import watools.General.raster_conversions as RC

def DownloadData(output_folder, latlim, lonlim, dataset, level = None):
    """
    This function downloads SoilGrids data from SoilGrids.org

    Keyword arguments:
    output_folder -- directory of the result
	 latlim -- [ymin, ymax] (values must be between -50 and 50)
    lonlim -- [xmin, xmax] (values must be between -180 and 180)
    level -- "sl1" .... "sl7"
    dataset -- ground dataset
    """
    # Define parameter depedent variables
    if dataset == "BLDFIE":
        nameEnd = os.path.join(output_folder, 'BulkDensity_%s_SoilGrids_kg-m-3.tif' %level)
        level_name = "%s_" %level
    if dataset == "CLYPPT":
        nameEnd = os.path.join(output_folder, 'ClayContentMassFraction_%s_SoilGrids_percentage.tif' %level)
        level_name = "%s_" %level        
    if dataset == "ORCDRC":
        nameEnd = os.path.join(output_folder, 'SoilOrganicCarbonContent_%s_SoilGrids_g_kg.tif' %level)        
        level_name = "%s_" %level
    if dataset == "OCSTHA":
        nameEnd = os.path.join(output_folder, 'SoilOrganicCarbonStock_%s_SoilGrids_tonnes-ha-1.tif' %level)        
        level_name = "%s_" %level
    if dataset == "CRFVOL":
        nameEnd = os.path.join(output_folder, 'CoarseFragmentVolumetric_%s_SoilGrids_percentage.tif' %level)        
        level_name = "%s_" %level
    if dataset == "SLTPPT":
        nameEnd = os.path.join(output_folder, 'SiltContentMassFraction_%s_SoilGrids_percentage.tif' %level)        
        level_name = "%s_" %level
    if dataset == "SNDPPT":
        nameEnd = os.path.join(output_folder, 'SandContentMassFraction_%s_SoilGrids_percentage.tif' %level)     
        level_name = "%s_" %level
    if dataset == "BDRICM":
        nameEnd = os.path.join(output_folder, 'DepthToBedrock_SoilGrids_cm.tif') 
        level_name = ""
    if dataset == "BDTICM":
        nameEnd = os.path.join(output_folder, 'AbsoluteDepthToBedrock_SoilGrids_cm.tif') 
        level_name = ""
    if dataset == "BDRLOG":
        nameEnd = os.path.join(output_folder, 'PredictedProbabilityOfOccurrence_SoilGrids_percentage.tif') 
        level_name = ""

    if not os.path.exists(nameEnd):
        
        # Create trash folder
        output_folder_trash = os.path.join(output_folder, "Trash")
        if not os.path.exists(output_folder_trash):
            os.makedirs(output_folder_trash)
    
        # Download, extract, and converts all the files to tiff files
        try:
            # Download the data from
            output_file = Download_Data(output_folder_trash, level_name, dataset)
    
            # Clip the data
            RC.Clip_Dataset_GDAL(output_file, nameEnd, latlim, lonlim)
    
        except:
            print("Was not able to create the wanted dataset")
            
        try:
            shutil.rmtree(output_folder_trash)  
        except:
            print("Was not able to remove the trash bin")

    return()

def Download_Data(output_folder_trash, level_name, dataset):
    """
    This function downloads the DEM data from the HydroShed website

    Keyword Arguments:
    output_folder_trash -- Dir, directory where the downloaded data must be
                           stored
    level_name -- "sl1_" .... "sl7_" or ""
    dataset -- ground dataset                           
    """
    try:
        # Define the filename
        filename = "%s_M_%s250m.tif" %(dataset,level_name)
        local_filename = os.path.join(output_folder_trash, filename)
        
        if not os.path.exists(local_filename):
            # Open the FTP connection
            ftp = FTP("ftp.soilgrids.org", "", "")
            ftp.login()
            
            # Go to the right path
            pathFTP = "data/recent"
            ftp.cwd(pathFTP)
            
            # Download the dataset
            lf = open(local_filename, "wb")
            ftp.retrbinary("RETR " + filename, lf.write, 8192)
            lf.close()
 
    except:
        print("Was not able to download the SoilGrids database, Database: %s level: %s" %(dataset, level_name))

    return(local_filename)
    

