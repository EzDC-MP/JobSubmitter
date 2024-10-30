#!/usr/bin/env python3
'''
compile a targeted impl of hpcg / hpg-mxp
using cmake

We suppose here that we already have required modules. This is simply
for compiling and to be called as a task (ie; msub)
'''
import os
import sys

def compile(options, buildPath, hpcgPath):
    os.chdir(hpcgPath)
    allOptions = "-B"+buildPath+" "+options
    print(allOptions)
    os.system("cmake "+allOptions)
    os.chdir(buildPath)
    os.system("make -j6")
    os.system("module list > build.log")
    os.system("echo "+options+" >> build.log")

if __name__ == "__main__":
    print(sys.argv)
    opt = sys.argv[1]
    buildPath = sys.argv[2]
    hpcgPath = sys.argv[3]
    compile(opt, buildPath, hpcgPath)
    exit()
