# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels and Gonzalo Espinoza
         UNESCO-IHE 2016
Contact: t.hessels@unesco-ihe.org
         g.espinoza@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect


Description:
This module contains scripts used to download Level 1 data (data directly from web).

Products                      Dates                             Password
ALEXI (daily)                 2005/01/01-2016/12/31             WA+ FTP
ALEXI (monthly)               2005/01/01-2016/12/31             WA+ FTP                         
ASCAT (daily)                 2007/01/01-now                    VITO
CFSR (daily)                  1979/01/01-now                    -
CHIRPS (daily)                1981/01/01-now                    -
CHIRPS (monthly)              1981/01/01-now                    -
CMRSET (monthly)              2000/01/01-2012/12/31             WA+ FTP
DEM                           -                                 -
ECMWF                         1979/01/01-now                    ECMWF_API
ETmonitor (monthly)           2008/01/01-2013/12/31             WA+ FTP    
GLDAS                         2000/01/01-now                    NASA
GLEAM (daily)                 2007/01/01-2017/12/31             GLEAM
GLEAM (monthly)               2007/01/01-2017/12/31             GLEAM            
HiHydroSoil                   -                                 WA+ FTP 
JRC                           -                                 -
MCD43 (daily)                 2000/02/24-now                    NASA
MOD10 (8-daily)               2000/02/18-now                    NASA
MOD11 (daily)                 2000/02/24-now                    NASA
MOD11 (8-daily)               2000/02/18-now                    NASA
MOD12 (yearly)                2001/01/01-2013/12/31             NASA
MOD13 (16-daily)              2000/02/18-now                    NASA
MOD15 (8-daily)               2000/02/18-now                    NASA
MOD16 (8-daily)               2000/01/01-2014/12/31             NASA
MOD16 (monthly)               2000/01/01-2014/12/31             NASA
MOD17 (8-daily GPP)           2000/02/18-now                    NASA
MOD17 (yearly NPP)            2000/02/18-2015/12/31             NASA
MOD9 (daily)                  2000/02/24-now                    NASA
MSWEP (daily)                 1979/01/01-now                    MSWEP
MSWEP (monthly)               1979/01/01-now                    MSWEP
MYD13 (16-daily)              2000/02/18-now                    NASA
RFE (daily)                   2001/01/01-now                    -
RFE (monthly)                 2001/01/01-now                    -                  
SEBS (monthly)                2000/03/01-2015/12/31             WA+ guest FTP
SSEBop (monthly)              2003/01/01-2014/10/31             WA+ FTP 
SoilGrids                     -                                 -
TRMM (daily)                  1998/01/01-2018/06/29             NASA
TRMM (monthly)                1998/01/01-2018/06/30             NASA
TWC                           -                                 WA+ guest FTP 

Examples:
from watools import Collect
help(Collect)
dir(Collect)
"""

from watools.Collect import TRMM, GLDAS, ALEXI, CHIRPS, DEM, CFSR, MOD9, MOD10, MOD11, MOD12, MOD13, MOD15, MOD16, MOD17, MCD43, MYD13, GLEAM, HiHydroSoil, ECMWF, RFE, JRC, TWC, ETmonitor, SEBS, SSEBop, CMRSET, MSWEP, ASCAT, SoilGrids, FEWS, PROBAV, GPM

__all__ = ['TRMM', 'GLDAS', 'ALEXI', 'CHIRPS', 'DEM', 'CFSR', 'MOD9', 'MOD10', 'MOD11', 'MOD12', 'MOD13', 'MOD15', 'MOD16', 'MOD17', 'MCD43', 'MYD13', 'GLEAM', 'HiHydroSoil', 'ECMWF', 'RFE', 'JRC', 'TWC', 'ETmonitor', 'SEBS', 'SSEBop', 'CMRSET', 'MSWEP', 'ASCAT', 'SoilGrids', 'FEWS', 'PROBAV', 'GPM']

__version__ = '0.1'
