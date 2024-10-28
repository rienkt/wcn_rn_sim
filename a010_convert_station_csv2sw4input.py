#!/usr/bin/env python
from __future__ import print_function
"""
  NEW.PY variables < infile > outfile

  <ADD_DESCRIPTION_HERE>


  * PARAMETERS




  Author : Rie Nakata
  Initial release :

"""
__author__ = "Rie Nakata"


#==============================================================================
#                                                                     MODULES
#==============================================================================

import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
import os, sys
import pandas as pd 

from collections import OrderedDict


#import rn.plot.format as rn_format

#import rn.rsf.model as rn_model
#import rn.bin.model as rn_model

#==============================================================================
#                                                                   PARAMETERS 
#==============================================================================

datadir = '../data/stations/'
#pngdir_top = '../png/'


fin = datadir + '/stations.csv'
fout = datadir + '/a010_sw4input.txt'
#==============================================================================
#                                                              LOCAL FUNCTIONS 
#==============================================================================

#==============================================================================
#                                                                       MAIN
#==============================================================================

df = pd.read_csv( fin ) 

#network,station,longitude,latitude,start_date,end_dateK#

df = df.drop_duplicates( subset=['station'] )

outlines = []
for index, station in df.iterrows() :
  outlines.append( 'rec lat=%f lon=%f depth=0.0 sta=%s.%s variables=velocity hdf5format=1 nsew=1'%( station.latitude, station.longitude, station.network, station.station ) )

with open( fout, 'w' ) as f :
  f.write( '\n'.join( outlines )  )






