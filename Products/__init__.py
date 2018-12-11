# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels and Gonzalo Espinoza
         UNESCO-IHE 2016
Contact: t.hessels@unesco-ihe.org
         g.espinoza@unesco-ihe.org
Repository: https://github.com/wateraccounting/wa
Module: Products


Description:
This module contains scripts used to create WA+ products (data directly from web).

Products                      Dates                             Password                        
ETens (monthly)               2003/01/01-2014/12/31             WA+ FTP
ETref (daily)                 2000/01/01-now                    NASA
ETref (monthly)               2000/01/01-now                    NASA

Examples:
from watools import Products
help(Products)
dir(Products)
"""

from watools.Products import ETref
from watools.Products import ETens
from watools.Products import SoilGrids

__all__ = ['ETref', 'ETens', 'SoilGrids']

__version__ = '0.1'