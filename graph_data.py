#!/usr/bin/env python3
'''
Python script to plot data obtained with data_jobs
'''
    
import os
import sys
import importlib.util
import matplotlib.pyplot as plt
import numpy as np
import data_jobs

### Variable declaration. These should be changed in a given config file. ###
GRAPHDIR = None
FILTER_IN = None
FILTER_EXCLUDE = None   

def load_conf(source):
    '''
    load config file at source as the module 'JobsubmitterConfig'.
    '''

    spec = importlib.util.spec_from_file_location("JobsubmitterConfig", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules["JobsubmitterConfig"] = module
    spec.loader.exec_module(module)
    
    global FILTER_IN, FILTER_EXCLUDE, GRAPHDIR, BUILDDIR

    FILTER_IN = module.graphIN
    FILTER_EXCLUDE = module.graphEXCLUDE
    GRAPHDIR = module.GRAPHDIR
    BUILDDIR = module.BUILDDIR
    return 

def createHTML():
    os.system('touch graph.html')
    os.system('echo "<div>various graphs</div>" > graph.html')
    files = os.listdir()
    print(files)
    for f in files:
        if (f.find('.png') != -1):
            os.system('echo \'<img src="'+f+'">\'>> graph.html')
    return

def sortAxes(values,names):
    return list(zip(*sorted(zip(values, names), reverse=True)))

def colorGrad(n):
    cmap = plt.cm.get_cmap('viridis')
    points = np.linspace(0,1,n,False)
    return [cmap(a) for a in points] 

def pruneName(name):
    parts = name.split(".")
    """if (parts[0].find("hpgmp") != -1):
        parts[0] = "hpgmp"
    elif (parts[0].find("hpcg") != -1):
        parts[0] = "hpcg"
    else:
        return name
    """
    return parts[0]+"\n"+parts[1].replace("-","\n")  

def tofloat(a):
    if a!='':
        return float(a)
    else:
        return 0

#----------------------------
def graphGflops(DATA):
    try:
        GFLOPS = [float(DATA[a]["GFLOP/sTotal"]) for a in DATA]
        NAMES = [pruneName(a) for a in DATA]
        
        GFLOPS, NAMES = sortAxes(GFLOPS,NAMES)

        fig, ax = plt.subplots()
        fig.set_figwidth(len(NAMES)*1.5)
        
        bar_container = ax.bar(NAMES, GFLOPS, color=colorGrad(len(GFLOPS)))
        ax.set(ylabel='GFLOP/s', title='GFLOP/s comparaison')
        labels = [f'{x}' for x in GFLOPS]
        # ^ not in bar_labels bc savfig messes up fmt= idk why
        ax.bar_label(bar_container, labels=labels, fontsize=8)
        #plt.setp(ax.get_xticklabels(), rotation=10
        #        , horizontalalignment='right')
        plt.savefig("Gflops.png", format="png"
                , bbox_inches='tight', pad_inches=0.2)
        plt.clf()
    except KeyError:
        print("No GFLOPS/sTotal key found.")
    return 

#----------------------------
def graphBW(DATA):
    try:
        BW = [tofloat(DATA[a]["B/W"]) for a in DATA]
        NAMES = [pruneName(a) for a in DATA]
        
        BW, NAMES = sortAxes(BW,NAMES)

        fig, ax = plt.subplots()
        fig.set_figwidth(len(NAMES)*1.5)
        
        bar_container = ax.bar(NAMES, BW, color=colorGrad(len(BW)))
        ax.set(ylabel='Memory Bandwidth GB/s', title='Bandwidth Comparaison')
        labels = [f'{x}' for x in BW]
        # ^ not in bar_labels bc savfig messes up fmt= idk why
        ax.bar_label(bar_container, labels=labels, fontsize=8)
        #plt.setp(ax.get_xticklabels(), rotation=10
        #        , horizontalalignment='right')
        plt.savefig("BW.png", format="png"
                , bbox_inches='tight', pad_inches=0.2)
        plt.clf()
    except KeyError:
        print("No B/W key found.")
    return 

#----------------------------
def graphGflopsDetails(DATA):
    names   = [pruneName(a) for a in DATA]
    #print("AAAAAAAAAA")
    print(names)
    fields = { 
    "DDOT"    : [tofloat(DATA[a]["DDOT"]) for a in DATA]
    ,"WAXPBY" : [tofloat(DATA[a]["WAXPBY"]) for a in DATA]
    ,"SpMV"   : [tofloat(DATA[a]["SpMV"]) for a in DATA]
    ,"MG"     : [tofloat(DATA[a]["MG"])  for a in DATA]
    }
     
    width = 0.2
    c = colorGrad(len(fields)) 
    i = 0
    x = np.arange(len(names))

    fig, ax = plt.subplots()   
    fig.set_figwidth(len(names)*1.5)
    
    ax.set(ylabel='GFLOP/s', title='GFLOP/s comparaison')
    
    for fname, values in fields.items():
        off = i*width
        bar_container = ax.bar(x+off, values, width=width, color=c[i]
                , label=fname)
        labels = [f'{z:1.2f}' for z in values]
        # ^ not in bar_labels bc savfig messes up fmt= idk why
        ax.bar_label(bar_container, labels=labels, fontsize=6)
        i+=1
   
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xticks(x + width*2, names)
    #ax.legend(loc='best')
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    
    plt.savefig("GflopsDetails.png", format="png"
        , bbox_inches='tight', pad_inches=0.2)
    plt.clf()

#----------------------------
def graphSkewDetails(DATA):
    names   = [pruneName(a) for a in DATA]
    fields = { 
    "SpMV"   : [tofloat(DATA[a]["SkewSpMV"]) for a in DATA]
    ,"MG"     : [tofloat(DATA[a]["SkewMG"])  for a in DATA]
    }
     
    width = 0.2
    c = colorGrad(len(fields)) 
    i = 0
    x = np.arange(len(names))

    fig, ax = plt.subplots()   
    fig.set_figwidth(len(names)*2)
    
    ax.set(ylabel='|x\'Ay-y\'Ax|/(2*||x||*||A||*||y||)/epsilon'
            , title='Departure from symmetry')
    
    for fname, values in fields.items():
        off = i*width*2
        bar_container = ax.bar(x+off, values, width=width, color=c[i]
                , label=fname)
        labels = [f'{z:.5E}' for z in values]
        # ^ not in bar_labels bc savfig messes up fmt= idk why
        ax.bar_label(bar_container, labels=labels, fontsize=6)
        i+=1
   
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xticks(x + width*1, names)
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
   
    plt.yscale('log')
    plt.savefig("Skewness.png", format="png"
        , bbox_inches='tight', pad_inches=0.2)
    plt.clf()

#----------------------------
def graphTimeDetails(DATA):
    names   = [pruneName(a) for a in DATA]
    fields = { 
    "DDOT"    : [tofloat(DATA[a]["DDOTt"]) for a in DATA]
    ,"WAXPBY" : [tofloat(DATA[a]["WAXPBYt"]) for a in DATA]
    ,"SpMV"   : [tofloat(DATA[a]["SpMVt"]) for a in DATA]
    ,"MG"     : [tofloat(DATA[a]["MGt"])  for a in DATA]
    }
    
    width = 0.9
    i = 1
    c = colorGrad(len(fields)+1) 
    bottom = np.zeros(len(names))

    fig, ax = plt.subplots() 
    fig.set_figwidth(len(names)*1.5)
    
    ax.set(ylabel='Time (s)', title='Time spent')
    
    for fname, values in fields.items():
        bar_container = ax.bar(names, values, width=width, color=c[i]
                , label=fname, bottom=bottom)
        labels = [f'{z}s' if z > 2 else '' for z in values]
        ax.bar_label(bar_container, labels=labels, fontsize=8
                , label_type='center')
        bottom += values
        i+=1
    
    #total time
    labels = [f'total={tofloat(DATA[z]["TotalTime"])}s' for z in DATA]
    bar_container = ax.bar(names, 0, width=width, label='', bottom=bottom)
    ax.bar_label(bar_container, labels=labels, fontsize=7)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    #plt.yscale("symlog")
    plt.ylim((0,max([tofloat(DATA[z]["TotalTime"]) for z in DATA])+5))
    plt.savefig("TimeDetails.png", format="png"
        , bbox_inches='tight', pad_inches=0.2)
    plt.clf()

#----------------------------
def graphFloat(DATA):
    names   = [pruneName(a) for a in DATA]
    fields = { 
    "DDOT"    : [tofloat(DATA[a]["DDOTf"]) for a in DATA]
    ,"WAXPBY" : [tofloat(DATA[a]["WAXPBYf"]) for a in DATA]
    ,"SpMV"   : [tofloat(DATA[a]["SpMVf"]) for a in DATA]
    ,"MG"     : [tofloat(DATA[a]["MGf"])  for a in DATA]
    }
    
    width = 0.9
    i = 1
    c = colorGrad(len(fields)+1) 
    bottom = np.zeros(len(names))

    fig, ax = plt.subplots() 
    fig.set_figwidth(len(names)*1.5)
    
    ax.set(ylabel='Amount', title='Floating Point operations')
   
    maxv = max([tofloat(DATA[z]["Totalf"]) for z in DATA])
    for fname, values in fields.items():
        bar_container = ax.bar(names, values, width=width, color=c[i]
                , label=fname, bottom=bottom)
        labels = [f'{z:.5E}' if (z/maxv > 0.1) else '' for z in values]
        ax.bar_label(bar_container, labels=labels, fontsize=8
                , label_type='center')
        bottom += values
        i+=1
    
    #total time
    labels = [f'total={tofloat(DATA[z]["Totalf"]):.5E}' for z in DATA]
    bar_container = ax.bar(names, 0, width=width, label='', bottom=bottom)
    ax.bar_label(bar_container, labels=labels, fontsize=7)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    #plt.yscale("symlog")
    plt.ylim((0,maxv*1.1))
    plt.savefig("Floatsnum.png", format="png"
        , bbox_inches='tight', pad_inches=0.2)
    plt.clf()

#----------------------------
def graphThreads(DATA):
    names   = [pruneName(a) for a in DATA]
    threadsn = [tofloat(DATA[a]["Threads"]) for a in DATA]

    threadsn, names = sortAxes(threadsn,names)

    fig, ax = plt.subplots()
    fig.set_figwidth(len(names)*1.5)
    
    bar_container = ax.bar(names, threadsn, color=colorGrad(len(threadsn)))
    ax.set(ylabel='Threads', title='Thread number')
    labels = [f'{x}' for x in threadsn]
    # ^ not in bar_labels bc savfig messes up fmt= idk why
    ax.bar_label(bar_container, labels=labels, fontsize=8)
    #plt.setp(ax.get_xticklabels(), rotation=10
    #        , horizontalalignment='right')
    plt.savefig("threads.png", format="png"
            , bbox_inches='tight', pad_inches=0.2)
    plt.clf()

#----------------------------
def graphIterations(DATA):
    names= [pruneName(a) for a in DATA]
    labels = [a.split("\n") for a in names] 

    fig, ax = plt.subplots()
    #fig.set_figwidth(len(names)*1.5)
    maxl = 0
    for a in DATA:
        if len(DATA[a]["iterations"]) > maxl:
            maxl = len(DATA[a]["iterations"])
    xax = range(1,maxl+1)
    print(xax)

    iterations = [DATA[a]["iterations"] for a in DATA]
    ax.set_yscale('log', base=2)

    for i in range(len(names)):
        print(i)
        print(names[i])
        xax = range(1, 350) 
        if (len(iterations[i]) != 350):
            iterations[i] = [iterations[i][a] if a < len(iterations[i]) else iterations[i][-1] 
                             for a in range(len(xax))]   
        ax.plot(xax, iterations[i]
                , marker='', markersize=3, label=labels[i][0]+" "+labels[i][2]
                , linewidth=0.6,)
    ax.set(ylabel='Residual norm', title='Residual evolution', xlabel="iterations")
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), title="mode")
    plt.show()
    plt.savefig("Iterations.png", format="png",bbox_inches="tight"
        , pad_inches=0.2)
    plt.clf()

#---------------------------
def run():
    graphdirExp = os.path.expandvars(GRAPHDIR)
    
    data_jobs.load_conf(sys.argv[1])
    DATA = data_jobs.run()
    iterDATA = data_jobs.getIterationData() 
    os.system('mkdir -p '+graphdirExp)
    os.chdir(graphdirExp)

    
    #/filtering
    topop = [] 
    for name in DATA:
        if FILTER_IN:
            boolin = 0
            for n in FILTER_IN:
                boolin = (n in name) or boolin
            if not(boolin):
                topop.append(name)

    for name in topop:
        DATA.pop(name)
    topop= []  
    
    for name in DATA:
        for n in FILTER_EXCLUDE:
            if n in name:
                topop.append(name)

    for name in topop:
        DATA.pop(name)
    #end filtering

    print("graphing :")
    for name in DATA:
        print("\t"+name)
    
    print(DATA)

    graphGflops(DATA)
    graphGflopsDetails(DATA)
    graphBW(DATA)
    graphFloat(DATA)
    graphTimeDetails(DATA)
    graphSkewDetails(DATA)
    graphThreads(DATA)
 
    graphIterations(iterDATA)
    
    createHTML()
    
if __name__ == "__main__":
    # load config passed in argv1
    if sys.argv[1]:
        load_conf(sys.argv[1])
    run()
