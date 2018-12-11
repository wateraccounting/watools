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
import numpy as np

# import WA+ modules
from watools.General import data_conversions as DC
from watools.General import raster_conversions as RC

def Topsoil(Dir, latlim, lonlim):
    """
    This function calculates the topsoil saturated soil characteristic (100cm)

    Keyword arguments:
    Dir -- 'C:/' path to the WA map
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    """
	
    print('/nCreate K Saturated map of the topsoil from SoilGrids')
    
    # Define parameters to define the topsoil
    SL = "sl3"
	
    Calc_Property(Dir, latlim, lonlim, SL)
	
    return

def Subsoil(Dir, latlim, lonlim):
    """
    This function calculates the subsoil saturated soil characteristic (15cm)

    Keyword arguments:
    Dir -- 'C:/' path to the WA map
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    """
	
    print('/nCreate K Saturated map of the subsoil from SoilGrids')
    
    # Define parameters to define the subsoil	
    SL = "sl6"
	
    Calc_Property(Dir, latlim, lonlim, SL)
	
    return
	
def Calc_Property(Dir, latlim, lonlim, SL):	
	
    return	


