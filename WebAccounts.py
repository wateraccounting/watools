# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 09:27:36 2016

@author: tih
"""


def Accounts(Type=None):

    User_Pass = {
     'NASA': ['', ''],
     'GLEAM': ['', ''],
     'FTP_WA': ['', ''],
     'MSWEP': ['', ''],
     'Copernicus': ['', ''],  #https://land.copernicus.vgt.vito.be/PDF/
     'VITO': ['', '']}     #https://www.vito-eodata.be/PDF/datapool/
	 
    Selected_Path = User_Pass[Type]

    return(Selected_Path)
