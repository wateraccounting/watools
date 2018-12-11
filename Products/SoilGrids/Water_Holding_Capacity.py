# -*- coding: utf-8 -*-
'''
Authors: Tim Hessels
         UNESCO-IHE 2018
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Products/SoilGrids
'''

# import general python modules
import os
import gdal
import numpy as np
import pandas as pd
import subprocess
import osr
import netCDF4
import glob

# import WA+ modules
from watools.General import data_conversions as DC
from watools.General import raster_conversions as RC

def Topsoil(Dir, latlim, lonlim):
    """
    This function calculates the topsoil Water Holding Capacity soil characteristic (15cm)

    Keyword arguments:
    Dir -- 'C:/' path to the WA map
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    """
	
    print('/nCreate Water Holding Capacity map of the topsoil from SoilGrids')
    
    # Define parameters to define the topsoil
    SL = "sl3"
	
    Calc_Property(Dir, latlim, lonlim, SL)
	
    return

def Subsoil(Dir, latlim, lonlim):
    """
    This function calculates the subsoil Water Holding Capacity soil characteristic (100cm)

    Keyword arguments:
    Dir -- 'C:/' path to the WA map
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    """
	
    print('/nCreate Water Holding Capacity map of the subsoil from SoilGrids')
    
	 # Define parameters to define the subsoil	
    SL = "sl6"
	
    Calc_Property(Dir, latlim, lonlim, SL)
	
    return
	
def Calc_Property(Dir, latlim, lonlim, SL):	
    
    import watools
    
    # Define level
    if SL == "sl3":
        level = "Topsoil"
    elif SL == "sl6":
        level = "Subsoil" 
    
    # check if you need to download
    filename_out_thetasat = os.path.join(Dir, 'SoilGrids', 'Theta_Sat' ,'Theta_Sat_%s_SoilGrids_kg-kg.tif' %level)
    if not os.path.exists(filename_out_thetasat):
       if SL == "sl3":
           watools.Products.SoilGrids.Theta_Sat.Topsoil(Dir, latlim, lonlim)
       elif SL == "sl6":
           watools.Products.SoilGrids.Theta_Sat.Subsoil(Dir, latlim, lonlim)

    filedir_out_whc = os.path.join(Dir, 'SoilGrids', 'Water_Holding_Capacity')
    if not os.path.exists(filedir_out_whc):
        os.makedirs(filedir_out_whc)    
               
    # Define theta field capacity output
    filename_out_whc = os.path.join(filedir_out_whc, 'Water_Holding_Capacity_%s_SoilGrids_mm-m.tif' %level)
    
    if not os.path.exists(filename_out_whc):
        
        # Get info layer
        geo_out, proj, size_X, size_Y = RC.Open_array_info(filename_out_thetasat)

        # Open dataset
        theta_sat = RC.Open_tiff_array(filename_out_thetasat)
        
        # Calculate theta field capacity
        theta_whc = np.ones(theta_sat.shape) * -9999   
        theta_whc = np.where(theta_sat < 0.301, 80, 450 * np.arccosh(theta_sat + 0.7) - 2 * (theta_sat + 0.7) + 20)        
               
        # Save as tiff
        DC.Save_as_tiff(filename_out_whc, theta_whc, geo_out, proj)
    return           
           
           
	
	


