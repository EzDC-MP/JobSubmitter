#!/usr/bin/env python3
'''
Python script to submit compile jobs to compile hpcg with different 
compiler parameters.
'''

import importlib.util
import compile
import os
import sys
import subprocess

#### Variable declaration. These should be changed in a given config file. ###
COMPILMOD = None
BUILDDIR = None
PATHS = None 
MACHINE = None
TIME = None
CORE = None

#load module python support - you SHOULD modify the path to your needs.
#exec(open('/usr/share/Modules/init/python.py').read())

def load_conf(source):
    '''
    load config file at source as the module 'JobsubmitterConfig'.
    '''

    spec = importlib.util.spec_from_file_location("JobsubmitterConfig", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules["JobsubmitterConfig"] = module
    spec.loader.exec_module(module)
    
    global COMPILMOD, BUILDDIR, PATHS, MACHINE, TIME, CORE

    COMPILMOD = module.COMPILMOD
    BUILDDIR = module.BUILDDIR
    PATHS = module.PATHS
    MACHINE = module.compMACHINE
    TIME = module.compTIME
    CORE = module.compCORE
    return 

#""" No op for local
def change_modules(mode):
    return
"""
def change_modules(mode):
    module('restore')
    for m in COMPILMOD[mode][0]: 
        module('load', m)
#"""

if __name__ == "__main__":
    # load config passed in argv1
    if sys.argv[1]:
        load_conf(sys.argv[1])
    else: #TODO fix this 
        print("Please provide config file. ex :\n ./compile_jobs.py conf.py")
        exit(1)

    paths_expanded = {} 
    for path in PATHS:
        paths_expanded[os.path.expandvars(path)] = PATHS[path]     
    local = os.getcwd()
    buildirExp = os.path.expandvars(BUILDDIR)
    for path in paths_expanded:
        for mode in COMPILMOD:

            #check if this compiling mode is required for current hpcg build
            if not(mode in paths_expanded[path]):
                continue

            #change_modules(mode)
    
            #build info
            #set specified compiler, otherwise take default cxx
            CXX = COMPILMOD[mode][3] 

            buildName = path.split('/')[-1]+"."+mode  
            #buildPath = local+"/builds/"+buildName+".build/"
            buildPath = buildirExp+"/"+buildName+".build/"
            buildOptions = "-DCMAKE_CXX_COMPILER="\
                    +CXX\
                    +" -DCMAKE_CXX_FLAGS="\
                    +"\""+COMPILMOD[mode][2]+"\""\
                    +COMPILMOD[mode][1]  
            
            os.system("mkdir -p "+buildPath)
                
            #Should be change to your needs
            call = "python3 ./compile.py "+"'"+buildOptions+"' "+buildPath+\
                " "+path
            print(call)
            os.system(call) #botch
            
            #save modules
            #module('save', buildName+".build")
    exit() 
