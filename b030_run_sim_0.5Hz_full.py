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
import matplotlib.pyplot as plt
import os, sys
import pandas as pd 

from collections import OrderedDict

#import rn.plot.format as rn_format

#import rn.rsf.model as rn_model
#import rn.bin.model as rn_model

#==============================================================================
#                                                                   PARAMETERS 
#==============================================================================

pnum = os.path.basename( __file__).split('_')[0]
print( pnum )

datadir_top = '../data/'
datadir_in_csv = datadir_top + '/from_rn_laptop/'
datadirout = datadir_top + '/%s_sim_0.5Hz/'%pnum



frun_template = '%s_run_template.sh'%pnum
fsw4input_template = '%s_template.sw4input'%pnum

fcsv = datadir_in_csv + '/c002_source_loc.csv'
fsta_csv = datadir_in_csv + '/c002_sta_sim.csv'

fout_sw4input_ = datadirout + '/%s_'%pnum +'EQ_%s.sw4input'
fout_run_ = datadirout + '%s_'%pnum + 'run_EQ_%s.sh'


flag_setting = 1
flag_batch = 0
#==============================================================================
#                                                              LOCAL FUNCTIONS 
#==============================================================================

#==============================================================================
#                                                                       MAIN
#==============================================================================

if not os.path.isdir( datadirout ) :
  print( 'creating %s'%datadirout )
  os.system( 'mkdir -p %s'%datadirout )

df = pd.read_csv( fcsv ) 
df_sta = pd.read_csv( fsta_csv ) 
#print( df ) 

#rec lat=37.918860 lon=-122.151790 depth=0.0 sta=BK.BRIB  hdf5format=1 nsew=1

reclines = []
for index, sta in df_sta.iterrows() :
  reclines.append( 'rec lat=%f lon=%f depth=0.0 sta=%s.%s hdf5format=1 nsew=1'%
        ( sta.latitude, sta.longitude, sta.network, sta.station )  )
#print( reclines )


with open( frun_template , 'r' ) as f :
  lines_run  = f.read().splitlines()

with open( fsw4input_template , 'r' ) as f :
  lines_sw4input  = f.read().splitlines()

if flag_setting == 1 :

  for index, src in df.iterrows() :
    xloc = int( src.id.split('_')[0] )
    zloc = int( src.id.split('_')[1] )
    if ( xloc%40  != 0  or zloc% 2000 != 0 ) :

      datadirout_sw4 = datadirout + '/output_EQ_%s'%src.id 
      fout_sw4input = fout_sw4input_%src.id
      fout_run      = fout_run_%src.id
      print( datadirout_sw4)
      if not os.path.isdir( datadirout_sw4 ) :
        print( 'creating %s'%datadirout_sw4 )
        os.system( 'mkdir -p %s'%datadirout_sw4 )

      #output sw4input
      lines_sw4input_out =  list( map( lambda x: 
                    x.replace('SID', 'EQ_%s'%src.id)
                     .replace('SDEPTH', '%f'%src.z )
                     .replace('SLAT', '%f'%src.lat)
                     .replace('SLON', '%f'%src.lon )
                     .replace('PNUM', '%s'%pnum ), lines_sw4input  ) ) + reclines

      

      with open( fout_sw4input, 'w' ) as f :
        f.write( '\n'.join( lines_sw4input_out ) )

      lines_run_out =  list( map( lambda x: 
                    x.replace('SID', 'EQ_%s'%src.id)
                    ,lines_run ) )
      with open( fout_run, 'w' ) as f :
        f.write( '\n'.join( lines_run_out ) )

if flag_batch == 1 :
  nnum = 0
  print( 'batch job submission' )
  os.chdir( datadirout ) 
  for index, src in df.iterrows() :
    #print( index, src )
    xloc = int( src.id.split('_')[0] )
    zloc = int( src.id.split('_')[1] )
    if ( xloc%40  != 0  or zloc% 2000 != 0 ) :
      print( 'we submit our job ',  xloc, zloc )
      nnum += 1 
      fout_run = fout_run_%src.id
      fexec = os.path.basename( fout_run )
      os.system( 'sbatch %s'%fexec )
  print( 'total number of simulations :', nnum )

