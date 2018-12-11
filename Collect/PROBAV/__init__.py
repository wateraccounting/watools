# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UNESCO-IHE 2018
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/ASCAT

Description:
This module downloads ASCAT data from
ftp.wateraccounting.unesco-ihe.org. Use the ASCAT.monthly function to
download and create daily ASCAT images in Gtiff format.
The data is available between 2007-01-01 till present.

The output file with the name 2003.01.01 contains the soil water index.

Examples:
from watools.Collect import ASCAT
ASCAT.daily(Dir='C:/Temp/', Startdate='2003-12-01', Enddate='2004-01-20',
           latlim=[-10, 30], lonlim=[-20, -10])
"""

from .five_daily import main as five_daily

__all__ = ['five_daily']

__version__ = '0.1'
