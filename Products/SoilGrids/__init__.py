# -*- coding: utf-8 -*-
"""
    Authors: Tim Hessels
             UNESCO-IHE 2018
    Contact: t.hessels@unesco-ihe.org
    Repository: https://github.com/wateraccounting/watools
    Module: Products/GridSoils

    Description:
    This product will calculate soil properties by using the GridSoils as basis. 
	Different soil characteristics can be estimated.
	The formulas are taken from the SoMoi model and the SoilGrids are taken from:
	ftp.soilgrids.org
"""

from watools.Products.SoilGrids import K_Sat
from watools.Products.SoilGrids import Theta_FC
from watools.Products.SoilGrids import Theta_Sat
from watools.Products.SoilGrids import Theta_Sat2
from watools.Products.SoilGrids import Theta_Res
from watools.Products.SoilGrids import Water_Holding_Capacity

__all__ = ['K_Sat', 'Theta_FC', 'Theta_Sat', 'Theta_Sat2', 'Theta_Res', 'Water_Holding_Capacity']

__version__ = '0.1'
