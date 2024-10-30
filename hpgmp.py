# Simple config file for Jobsubmitter #

# Compilation #
###############

#Dictionnary with different compile modes ; an entry looks like this :
# "name"0 : {"modules", "CMAKE FLAGS", "CXX FLAGS", "compiler"} 
COMPILMOD = { }
BUILDDIR = "/Where/to/put/builds"
PATHS = {"/Where/to/find/hpgmp" : ["which","compilmod","to","use"], 
         "/Other/bench/hpgmp-comp" : ["which","compilmod","to","use"]} 

#Cluster specific infos
compMACHINE = None
compTIME = None
compCORE = None

# Running #
###########
JOBDIR = "/Your/path/to/jobs" #script to execute to launch the bench. bc
#some clusters need SLURMs scripts and such to work. 
runIN = [] #if not empty, only names with theses susbstring will be run
runEXCLUDE = [] #if not empty, only namew without theses susbstring will be run

# Graphing # 
############
GRAPHDIR = "/Where/to/put/graphs"
graphIN = []
graphEXCLUDE = [] 
