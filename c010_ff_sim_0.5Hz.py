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

datadir_top = '../data/'
datadir_in_csv = datadir_top + '/from_rn_laptop/'
datadirout = datadir_top + '/c010_ff_sim_0.5Hz/'
datadir_rupture = datadir_top + '/from_rn_laptop/a000_from_arben/'



frun_template = 'c010_ff_run_template.sh'
fsw4input_template = 'c010_ff_template.sw4input'

#fcsv = datadir_in_csv + '/c001_source_loc.csv'
fsta_csv = datadir_in_csv + '/c001_sta_sim.csv'

fout_sw4input_ = datadirout + '/c010_FF_%s.sw4input'
fout_run_ = datadirout + 'c010_run_FF_%s.sh'


fhruptures = [
#'r0001_m4.50-1.8x1.8_s600-V5_Hayward_v5.5.0_HB',
#'r1001_m5.00-3.4x3.0_s700-V5_Hayward_v5.5.0_HB',
#'r2001_m5.50-8.0x4.0_s600-V5_Hayward_v5.5.0_HB'
'r0001_m4.50-1.8x1.8_s600-V5_Hayward_v5.5.0_HB',
'r1001_m5.00-3.4x3.0_s700-V5_Hayward_v5.5.0_HB',
'r2001_m5.50-8.0x4.0_s600-V5_Hayward_v5.5.0_HB'
]

fhtail = '.srf.h5'



#pngdir_top = '../png/'
#
## true models
#
## inverted models
#fvp_ = 'vp-%2.2d.rsf'
#fvs_ = 'vs-%2.2d.rsf'
#fden_ = 'den-%2.2d.rsf'
#
#
## slowness
#fgslp_ = 'gslp=%2.2d.rsf'
#fgsls_ = 'gsls=%2.2d.rsf'
#
#==============================================================================
#                                                              LOCAL FUNCTIONS 
#==============================================================================

#==============================================================================
#                                                                       MAIN
#==============================================================================

if not os.path.isdir( datadirout ) :
  print( 'creating %s'%datadirout )
  os.system( 'mkdir -p %s'%datadirout )

#df = pd.read_csv( fcsv ) 
df_sta = pd.read_csv( fsta_csv ) 
#print( df ) 

#rec lat=37.918860 lon=-122.151790 depth=0.0 sta=BK.BRIB  hdf5format=1 nsew=1

reclines = []
for index, sta in df_sta.iterrows() :
  reclines.append( 'rec lat=%f lon=%f depth=0.0 sta=%s.%s hdf5format=1 nsew=1'%
        ( sta.latitude, sta.longitude, sta.network, sta.station )  )
print( reclines )


with open( frun_template , 'r' ) as f :
  lines_run  = f.read().splitlines()

with open( fsw4input_template , 'r' ) as f :
  lines_sw4input  = f.read().splitlines()

for fhrupture in fhruptures :
  rid = fhrupture[:5]
  print( rid, fhrupture )
  frupture = datadir_rupture + fhrupture + fhtail
  afrupture = os.path.abspath( frupture )
  print( frupture )
  datadirout_sw4 = datadirout + '/output_%s'%fhrupture
  adatadirout_sw4 = os.path.abspath( datadirout_sw4 ) 
  
  fout_sw4input = fout_sw4input_%rid
  fout_run      = fout_run_%rid
  print( datadirout_sw4)
  if not os.path.isdir( datadirout_sw4 ) :
    print( 'creating %s'%datadirout_sw4 )
    os.system( 'mkdir -p %s'%datadirout_sw4 )

  #output sw4input
  lines_sw4input_out =  list( map( lambda x: 
                x.replace('DATADIROUT', adatadirout_sw4 )
                 .replace('FRUPTURE',afrupture  )
                 , lines_sw4input ) ) + reclines

  

  with open( fout_sw4input, 'w' ) as f :
    f.write( '\n'.join( lines_sw4input_out ) )

  lines_run_out =  list( map( lambda x: 
                x.replace('DATADIROUT', adatadirout_sw4 )
                .replace('RID', 'FF_%s'%rid)
                ,lines_run ) )
  with open( fout_run, 'w' ) as f :
    f.write( '\n'.join( lines_run_out ) )

print( 'batch job submission' )
os.chdir( datadirout ) 
#for index, src in df.iterrows() :
for fhrupture in fhruptures :
  rid = fhrupture[:5]
  fout_run      = fout_run_%rid
  print( fout_run )
  fexec = os.path.basename( fout_run )

  os.system( 'sbatch %s'%fexec )

