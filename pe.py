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
        print >> sys.stderr, "ERROR: Cannot read the file %s" % (fileName)
        raise SystemExit(1)




PROBLEM_LINE=r'\s*^(\\paragraph{)(.*)\s*}'
SOLUTION_LINE=r'\s*^\\paragraph\*{'

class Problems: 
    def __init__(self):
       self.problems=OrderedDict()
       self.keys=[]
       self.cmds=[]

    def addKeys(self, keyList):
        for k in keyList:
            k=k.strip()
            cmd=k.split(" ")[0].lower()
            if len(cmd)==0: 
                continue
            if cmd[0]=="#":
                continue
            args=" ".join(k.split(" ")[1:])
            if len(cmd)>0 and len(args)>0:
                self.cmds.append(cmd)
                self.keys.append(args)

    def processTex(self, tex):
        lines=readLines(tex)
        probName=""
        probBody=""
        probSolution=""

        for line in lines: 
            line=line.strip()

#            if len(line)==0:
#                continue

            if re.search(r'\\section', line, re.UNICODE)!=None:
                continue

            if re.search(r'\\subsection', line, re.UNICODE)!=None:
                continue

            if re.search(r'^%', line, re.UNICODE)!=None:
                continue

            match = re.search(PROBLEM_LINE, line, re.UNICODE)
            if match != None: 
                if match.group(2) != probName and probName!="":
                    if probName in self.problems.keys():
                        print >> sys.stderr, "WARNING: The key \"%s\" already in the database!" % (probName)
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
                probBody = '\n'.join([probBody, line])
            else:
                probSolution = '\n'.join([probSolution, line])

        if probName!="":
            if probName in self.problems.keys():
                print >> sys.stderr, "WARNING: The key \"%s\" already in the database!" % (probName)
            self.problems[probName] = [probBody, probSolution]

    def printProblems(self):
        for i in range(len(self.cmds)):
            cmd=self.cmds[i]
            key=self.keys[i]
            if cmd=="sse":
                print "\\section*{%s}" % (key)
            if cmd=="sss":
                print "\\subsection*{%s}" % (key)
            if cmd=="tex":
                print key
            key=key.lower()
            if cmd=="p" or cmd=="s":
                if not key in self.problems.keys():
                    print >> sys.stderr, "ERROR: \"%s\" not found!" % (key)
                    raise SystemExit(1)
                if cmd=="p":
                    print self.problems[key][0]
                if cmd=="s":
                    print self.problems[key][0]
                    print "\n%% solution"
                    print self.problems[key][1]
            
    def printSummary(self):
#        print "Problems in the datebase :: %d" % (len(self.problems.keys()))
        for i in range(len(self.problems.keys())):
            print "%d. %s" % (i, self.problems.keys()[i])



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
        db.printProblems()












