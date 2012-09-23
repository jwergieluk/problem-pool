#!/usr/bin/env python2

import math, sys, os, calendar




def readLines(fileName):
    try:
        with open(fileName, "r") as h:
            lines = h.readlines()
        return lines
    except IOError as e:
        print "ERROR: Cannot read the file %s" % fileName
        raise SystemExit







def printUsage():
    print "Problem extractor (c) Julian Wergieluk 2012, GPL"
    print "usage: %s [file]" % sys.argv[0]



if __name__ == "__main__":

    texFiles=[]
    db={}

    
    if len(sys.argv) <=1:
        printUsage()
        sys.exit()

    for f in sys.argv[1:]:
        lines = readFile(f)
        print lines[0]











