#Taken from https://github.com/anthony-cooper/modelRunner/blob/master/genericIEF.py
import os
import re

def genFileLines(genericIEF, events, scenarios):
    file = open(genericIEF,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:
        if re.search('<<~.*~>>', line): #Replace Event/Scenario Operators
            #Replace e# and s#, if suitable scenario exists
            for e in range(0, len(events)):
                line = line.replace('<<~e'+str(e)+'~>>',events[e])
            for s in range(0, len(scenarios)):
                line = line.replace('<<~s'+str(s)+'~>>',scenarios[s])

            #Replace remaining with either e0, s0 or failing EVENT, SCENARIO
            try:
                line = re.sub('<<~e*.~>>',events[0],line)
            except:
                line = re.sub('<<~e*.~>>','EVENT',line)
            try:
                line = re.sub('<<~s*.~>>',scenarios[0],line)
            except:
                line = re.sub('<<~s*.~>>','SCENARIO',line)

        fileLines.append(line)

    file.close

    return fileLines

def genFileName(fileName, events, scenarios):
    if re.search('~.*~', fileName): #Replace Event/Scenario Operators
        #Replace e# and s#, if suitable scenario exists
        for e in range(0, len(events)):
            fileName = fileName.replace('~e'+str(e)+'~',events[e])
        for s in range(0, len(scenarios)):
            fileName = fileName.replace('~s'+str(s)+'~',scenarios[s])

        #Replace remaining with either e0, s0 or failing EVENT, SCENARIO
        try:
            fileName = re.sub('~e*.~',events[0],fileName)
        except:
            fileName = re.sub('~e*.~','EVENT',fileName)
        try:
            fileName = re.sub('~s*.~',scenarios[0],fileName)
        except:
            fileName = re.sub('~s*.~','SCENARIO',fileName)
    return fileName
