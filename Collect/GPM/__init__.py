# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UNESCO-IHE 2019
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/GPM


Description:
This module downloads GPM (daily) and GPM (monthly) data from
ftp://disc2.nascom.nasa.gov. Use the GPM.daily or GPM.monthly functions to
download and create daily or monthly GPM images in Gtiff format.
The TRMM data is available since 2014-03-01 till present

Examples:
from wa.Collect import GPM
GPM.daily(Dir='C:/Temp/', Startdate='2014-03-01', Enddate='2015-03-01',
           latlim=[-10, 30], lonlim=[-20, 120])
GPM.monthly(Dir='C:/Temp/', Startdate='2014-03-01', Enddate='2015-03-01',
             latlim=[-10, 30], lonlim=[-20, 120])
"""

from .daily import main as daily
from .monthly import main as monthly

__all__ = ['daily', 'monthly']

__version__ = '0.1'
