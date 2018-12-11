# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels and Gonzalo Espinoza
         UNESCO-IHE 2017
Contact: t.hessels@unesco-ihe.org
         g.espinoza@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/SSEBop

Restrictions:
The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the SSEBop developers.

Description:
This module downloads SSEBop data from
ftp.wateraccounting.unesco-ihe.org. Use the SSEBop.monthly function to
download and create monthly SSEBop images in Gtiff format.
Data is available between 2003-01-01 till 2014-10-31. If the FTP version is used
The data goes till present if the V4 version is used (Default)

Examples:
from watools.Collect import SSEBop
SSEBop.ET_monthly(Dir='C:/Temp/', Startdate='2008-12-01', Enddate='2011-01-20',
           latlim=[-10, 30], lonlim=[-20, -10])
"""

from .ET_monthly import main as ET_monthly
from .ETpot_daily import main as ETpot_daily
__all__ = ['ET_monthly', 'ETpot_daily']

__version__ = '0.1'
