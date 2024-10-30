#!/usr/bin/env python3
'''
Python script to collect data from finished jobs
Data are ripped from the benchmark txt files produced
'''

import importlib.util
import os
import sys
import numpy as np

BUILDDIR = "$PWD/builds"

#TODO get machine spec someway somehow.

# where collected info reside. Dictionnaries within dictionnaries.
# Each different builds have an entry here
DATA = {}

#The fields we want to extract from the .txt
#Get the value fromt the line with the specified substr.
FIELDS = { 
        "Global nx" : "nx",
        "Global ny" : "ny",
        "Global nz" : "nz",
        
        "GB/s Summary::Raw Total B/W" : "B/W",

        "GFLOP/s Summary::Raw DDOT"     : "DDOT",
        "GFLOP/s Summary::Raw WAXPBY"   : "WAXPBY",
        "GFLOP/s Summary::Raw SpMV"     : "SpMV",
        "GFLOP/s Summary::Raw MG"       : "MG",
        "GFLOP/s Summary::Raw Total"    : "GFLOP/sTotal",

        "Benchmark Time Summary::DDOT"  : "DDOTt",
        "Benchmark Time Summary::WAXPBY": "WAXPBYt",
        "Benchmark Time Summary::SpMV"  : "SpMVt",
        "Benchmark Time Summary::MG"    : "MGt",
        "Benchmark Time Summary::Total" : "TotalTime",

        "Machine Summary::Threads per processes": "Threads",

        "Departure for SpMV" : "SkewSpMV",
        "Departure for MG"   : "SkewMG",

        "Floating Point Operations Summary::Raw DDOT"   : "DDOTf",
        "Floating Point Operations Summary::Raw WAXPBY" : "WAXPBYf",
        "Floating Point Operations Summary::Raw SpMV"   : "SpMVf",
        "Floating Point Operations Summary::Raw MG"     : "MGf",
        "Floating Point Operations Summary::Total"      : "Totalf",
}

def load_conf(source):
    '''
    load config file at source as the module 'JobsubmitterConfig'.
    '''

    spec = importlib.util.spec_from_file_location("JobsubmitterConfig", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules["JobsubmitterConfig"] = module
    spec.loader.exec_module(module)
    
    global BUILDDIR 

    BUILDDIR = module.BUILDDIR
    return 

def extractValue(data, field):
    index = data.find(field)
    return data[index::].partition("=")[2].partition("\n")[0]

def findBenchFile(l):
    for entry in l:
        if entry[0] == "H":
            return entry

def findIterationFile(l):
    for entry in l:
        if entry == "iterations.csv":
            return entry

def extractLines(f, n):
    with open(f, 'r') as w:
        return w.readlines()[0:n] 

def getIterationData():
    buildirExp = os.path.expandvars(BUILDDIR)
    os.chdir(buildirExp)
    builds = os.listdir()
    #print(builds)
    
    iterDATA = {} 
    
    for buildName in builds:
        #cd into current build
        os.chdir(buildirExp+"/"+buildName)
        filename = findIterationFile(os.listdir())
        if (filename == None):
            print("Cannot find "+buildName+" iteration.csv", file=sys.stderr)
            continue

        iterDATA[buildName] = {"name":buildName} 
        currData = iterDATA[buildName] 
        currData["fullname"] = filename
        currData["info"] = extractLines(filename,3)
        currData["iterations"] = np.genfromtxt(filename, dtype="float")
    return iterDATA

#for module inclusion - allow a simple function call to get DATA
def run():
    buildirExp = os.path.expandvars(BUILDDIR)
    os.chdir(buildirExp)
    builds = os.listdir()
    #print(builds)

    for buildName in builds:
        #cd into current build
        os.chdir(buildirExp+"/"+buildName)
        filename = findBenchFile(os.listdir())
        if (filename == None):
            print("Cannot find "+buildName+" bench", file=sys.stderr)
            continue

        #create entry
        DATA[buildName] = {"name":buildName}
        currData = DATA[buildName] 
        currData["fullname"] = filename
        
        #extract Benchmark.txt
        file = open(filename, 'r')
        rawtxt = file.read()
        file.close()
        
        #populate dict
        for field in FIELDS:
            currData[FIELDS[field]] = extractValue(rawtxt,field)
    return DATA

if __name__ == "__main__":
    # load config passed in argv1
    if sys.argv[1]:
        load_conf(sys.argv[1])
        print(BUILDDIR)
    iterDATA = getIterationData()
    print(iterDATA)
