#!/usr/bin/env python3
'''
Python script to run hpcg benchmarks jobs. 
each folder is a different jobs
'''

import os
import sys
import importlib.util

### Variable declaration. These should be changed in a given config file. ###
BUILDDIR = None
JOBDIR = None
FILTER_IN = None
FILTER_EXCLUDE = None   

#list of executable we might want to run ; since each builds do not 
#yield the same names sometimes.
EXEC = ["xhpcg","xhpgmp"] 

#Different start combination
hpcgDats = ["""
HPCG benchmark input file
Sandia National Laboratories; University of Tennessee, Knoxville
64 64 64
500
"""]

#load module python support
#exec(open('/usr/share/Modules/init/python.py').read())

def load_conf(source):
    '''
    load config file at source as the module 'JobsubmitterConfig'.
    '''

    spec = importlib.util.spec_from_file_location("JobsubmitterConfig", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules["JobsubmitterConfig"] = module
    spec.loader.exec_module(module)
    
    global FILTER_IN, FILTER_EXCLUDE, BUILDDIR, JOBDIR

    FILTER_IN = module.runIN
    FILTER_EXCLUDE = module.runEXCLUDE
    BUILDDIR = module.BUILDDIR
    JOBDIR = module.JOBDIR
    return 

if __name__ == "__main__":
    # load config passed in argv1
    if sys.argv[1]:
        load_conf(sys.argv[1])

    buildirExp = os.path.expandvars(BUILDDIR)
    jobdirExp = os.path.expandvars(JOBDIR)
    os.chdir(buildirExp)
    builds = os.listdir()
    
    #filtering
    #TODO separate this in other function.
    topop = [] 
    for name in builds:
        if FILTER_IN:
            boolin = 0
            for n in FILTER_IN:
                boolin = (n in name) or boolin
            if not(boolin):
                topop.append(name)

    for name in topop:
        builds.remove(name)
    topop = []  

    for name in builds:
        for n in FILTER_EXCLUDE:
            if n in name:
                topop.append(name)
    
    for name in topop:
        builds.remove(name)
    #end filtering

    for buildName in builds:
        #module('restore',buildName)
        os.chdir(buildirExp+"/"+buildName)
        
        os.system("cat > hpcg.dat <<EOL"+hpcgDats[0]+"EOL")
        os.system("cat > hpgmp.dat <<EOL"+hpcgDats[0]+"EOL") 
       
        for script in os.listdir(jobdirExp):
            os.system("cp "+jobdirExp+"/"+script+" ./"+script)
            call = "./"+script
            os.system(call)
