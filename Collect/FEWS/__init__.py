# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels and Gonzalo Espinoza
         UNESCO-IHE 2017
Contact: t.hessels@unesco-ihe.org
         g.espinoza@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/FEWS

Description:
This module downloads FEWS data from
ftp.wateraccounting.unesco-ihe.org. Use the FEWS.ETpot_daily function to
download and create monthly FEWS images in Gtiff format.
Data is available between 2003-01-01 till 2014-10-31. If the FTP version is used
The data goes till present if the V4 version is used (Default)

Examples:
from watools.Collect import SSEBop
FEWS.ETpot_daily(Dir='C:/Temp/', Startdate='2008-12-01', Enddate='2011-01-20',
           latlim=[-10, 30], lonlim=[-20, -10])
"""

from .ETpot_daily import main as ETpot_daily
__all__ = ['ETpot_daily']

__version__ = '0.1'
