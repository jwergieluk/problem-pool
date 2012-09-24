#!/usr/bin/env python2

def printUsage():
    print "Problem extractor (c) Julian Wergieluk 2012, GPL"
    print "usage: %s [command] [key file] [problem file 1] [.. [problem file n]] " % sys.argv[0]


import math, sys, os, calendar, re
from collections import OrderedDict

def readLines(fileName):
    try:
        with open(fileName, "r") as h:
            lines = h.readlines()
        return lines
    except IOError as e:
        print "ERROR: Cannot read the file %s" % fileName
        raise SystemExit




PROBLEM_LINE=r'\s*(\\paragraph{)(.*)\.\s*}'
SOLUTION_LINE=r'\s*\\paragraph\*{'

class Problems: 
    def __init__(self):
       self.problems=OrderedDict()
       self.keys=[]

    def addKeys(self, keyList):
        for k in keyList:
            self.keys.append(k.strip().lower())

    def processTex(self, tex):
        lines=readLines(tex)
        probName=""
        probBody=""
        probSolution=""

        for line in lines: 
            line=line.strip()

            if len(line)==0:
                continue

            if re.search(r'\\section', line, re.UNICODE)!=None:
                continue

            match = re.search(PROBLEM_LINE, line, re.UNICODE)
            if match != None: 
                if match.group(2) != probName and probName!="":
                    if probName in self.problems.keys():
                        print "WARNING: The key \"%s\" already in the database!" % (probName)
                    self.problems[probName] = [probBody, probSolution]

                probName=match.group(2).strip().lower()
                probBody=line
                probSolution=""
                continue

            match = re.search(SOLUTION_LINE, line, re.UNICODE)
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

    def printProblems(self, solutions):
        for p in self.keys:
            if len(p)>0 and p in self.problems.keys():
                print self.problems[p][0]
                if solutions:
                    print self.problems[p][1]
                print 
            
    def printSummary(self):
        print "Problems in the datebase :: %d" % (len(self.problems.keys()))
        print "Keys :: ", self.keys 
        print "Keys :: ", self.problems.keys()



if __name__ == "__main__":

    db=Problems()
    
    if len(sys.argv)<4:
        printUsage()
        sys.exit()

    cmd=sys.argv[1]
    db.addKeys(readLines(sys.argv[2]))

    for f in sys.argv[3:]:
        db.processTex(f)
        
    if cmd=="s":
        db.printSummary()
    if cmd=="p":
        db.printProblems(False)
    if cmd=="ps":
        db.printProblems(True)












