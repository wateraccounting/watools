# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
Contact: t.hessels@un-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Collect/SoilGrids


Description:


Examples:



"""
from .Bulk_Density import main as Bulk_Density
from .Clay_Content import main as Clay_Content
from .Absolute_Depth_To_Bedrock import main as Absolute_Depth_To_Bedrock
from .Coarse_Fragment_Volumetric import main as Coarse_Fragment_Volumetric
from .Depth_To_Bedrock import main as Depth_To_Bedrock
from .Organic_Carbon_Content import main as Organic_Carbon_Content
from .Organic_Carbon_Stock import main as Organic_Carbon_Stock
from .Predicted_Probability_Of_Occurrence import main as Predicted_Probability_Of_Occurrence
from .Sand_Content import main as Sand_Content
from .Silt_Content import main as Silt_Content

__all__ = ['Bulk_Density','Clay_Content','Absolute_Depth_To_Bedrock','Coarse_Fragment_Volumetric','Depth_To_Bedrock','Organic_Carbon_Content','Organic_Carbon_Stock','Predicted_Probability_Of_Occurrence','Sand_Content','Silt_Content']

__version__ = '0.1'
