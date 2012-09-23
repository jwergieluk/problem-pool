#!/usr/bin/env python2

def printUsage():
    print "Problem extractor (c) Julian Wergieluk 2012, GPL"
    print "usage: %s [file]" % sys.argv[0]


import math, sys, os, calendar, re


def readLines(fileName):
    try:
        with open(fileName, "r") as h:
            lines = h.readlines()
        return lines
    except IOError as e:
        print "ERROR: Cannot read the file %s" % fileName
        raise SystemExit




PROBLEM_LINE=r'\s*(\\paragraph{)([\w*\s]+)\.\s*}'
SOLUTION_LINE=r'\s*\\paragraph\*{'

class Problems: 
    def __init__(self):
       self.problems={}

    def processTex(self, tex):
        lines=readLines(tex)
        probName=""
        probBody=""
        probSolution=""

        for line in lines: 
            line=line.strip()
            match = re.search(PROBLEM_LINE, line)
            if match != None: 
                if match.group(2) != probName and probName!="":
                    if probName in self.problems.keys():
                        print "WARNING: The key \"%s\" already in the database!" % (probName)
                    self.problems[probName] = [probBody, probSolution]

                probName=match.group(2)
                probBody=line
                probSolution=""
                continue

            match = re.search(SOLUTION_LINE, line)
            if match != None: 
                probSolution = line
                continue

            if len(probSolution) == 0:
                probBody = ' '.join([probBody, line])
            else:
                probSolution = ' '.join([probSolution, line])

        if probName!="":
            if probName in self.problems.keys():
                print "WARNING: The key \"%s\" already in the database!" % (probName)
            self.problems[probName] = [probBody, probSolution]

    def printProblems(self):
        for p in self.problems.keys():
            print "Problem:", p
            print "Body:", self.problems[p][0]
            print "Solution:", self.problems[p][1]
            
            



if __name__ == "__main__":

    db=Problems()

    
    if len(sys.argv) <=1:
        printUsage()
        sys.exit()

    for f in sys.argv[1:]:
        db.processTex(f)
        
    db.printProblems()












