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
datadirout = datadir_top + '/b010_sim_0.5Hz/'



frun_template = 'b010_run_template.sh'
fsw4input_template = 'b010_template.sw4input'

fcsv = datadir_in_csv + '/c000_source_loc.csv'

fout_sw4input_ = datadirout + '/b010_EQ_%s.sw4input'
fout_run_ = datadirout + 'b010_run_EQ_%s.sh'



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

df = pd.read_csv( fcsv ) 
print( df ) 

with open( frun_template , 'r' ) as f :
  lines_run  = f.read().splitlines()

with open( fsw4input_template , 'r' ) as f :
  lines_sw4input  = f.read().splitlines()

for index, src in df.iterrows() :
  print( index, src )
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
                 .replace('SLON', '%f'%src.lon ), lines_sw4input ) )



  with open( fout_sw4input, 'w' ) as f :
    f.write( '\n'.join( lines_sw4input_out ) )

  lines_run_out =  list( map( lambda x: 
                x.replace('SID', 'EQ_%s'%src.id)
                ,lines_run ) )
  with open( fout_run, 'w' ) as f :
    f.write( '\n'.join( lines_run_out ) )

print( 'batch job submission' )
os.chdir( datadirout ) 
for index, src in df.iterrows() :
  print( index, src )
  fout_run      = fout_run_%src.id
  fexec = os.path.basename( fout_run )

  os.system( 'sbatch %s'%fexec )

