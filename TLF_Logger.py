import os.path as path #Used for path commands
import pathlib #Used to rseolve relative paths; Requires python 3.4
from datetime import datetime #Used to format date/times
import re #Regular expressions, used for wildcard matching


def tlfLogger(tlfFile):
    loggedItems = []
    loggedItems.extend(tlfFileAssessment(tlfFile))

    return loggedItems

def tlfFileAssessment(textFile):
    loggedItems =[]
    #Read in file
    file = open(textFile,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:

        fileLines.append(line.split())

    file.close

    workingFolder=path.dirname(textFile)

    loggedItems.extend(tlfTextAssessment(fileLines))

    return loggedItems

def tlfTextAssessment(textBlock):
    loggedItems=[]
    cputime=''
    clocktime=''
    mxTime = ''
    time=''
    #4. Take list of lists (lines split into words) and handle
    text = iter(textBlock)
    for textLine in text:
        try: #Catch errors from short lines, needs to check in order of number of words
            if 'Mx' in textLine:
                mx = ''
                ckMx = False
                for item in textLine:
                    if ckMx:
                        if '.' in item:
                            mx=mx+item.ljust(4,'0')
                        else:
                            mx=mx+item.ljust(2,'0')
                    elif item == 'Mx':
                        ckMx = True

                time = float(textLine[1].split(':')[0])+float(float(textLine[1].split(':')[1])/60)+float(float(textLine[1].split(':')[2])/3600)
                if float(mx[4:]) == 0:
                    mxTime = time
                mx=''
                ckMx = False
            elif textLine[0].casefold()  == 'BUILD:'.casefold():
                loggedItems.append(('TUFLOW Build', textLine[1]))
            elif ''.join(textLine[:2]).casefold() == 'SimulationStarted:'.casefold():
                loggedItems.append(('Simulation Start Time', textLine[2] + ' ' + textLine[3]))
            elif ''.join(textLine[:2]).casefold() in ['SpecifiedEvents:'.casefold(),'SpecifiedScenarios:'.casefold()]:
                es = next(text)
                while es:
                    if es[0][1] == 'e':
                        loggedItems.append(('Event '+es[0][2],es[1]))

                    elif es[0][1] == 's':
                        loggedItems.append(('Scenario '+es[0][2],es[1]))
                    es = next(text)
            elif ''.join(textLine[:2]).casefold() in ['CPUTime:'.casefold()]:
                cputime = textLine[2]
            elif ''.join(textLine[:2]).casefold() in ['ClockTime:'.casefold()]:
                clocktime = textLine[2]
            elif ''.join(textLine[:2]).casefold() in ['SimulationFINISHED'.casefold()]:
                loggedItems.append(('Simulation Finished Clock Time',cputime))
                loggedItems.append(('Simulation Finished CPU Time',clocktime))
                while True:
                    try:
                        summary = next(text)
                        if ':' in ' '.join(summary):
                            loggedItems.append((' '.join(summary).split(':')[0],' '.join(summary).split(':')[1].split()[0]))
                            if ' '.join(summary).split(':')[0] == 'Peak Cumulative ME':
                                loggedItems.append(('Peak Cumulative ME Time',' '.join(summary).split(':')[1].split()[2]))

                    except:
                        break
            elif ''.join(textLine[:3]).casefold()  == '2DDomainTimesteps:'.casefold():
                timesteps = ''.join(textLine[3:]).split(',')
                for i in range(0, len(timesteps)):
                    if timesteps[i]:
                        loggedItems.append(('Timestep Domain '+str(i+1), timesteps[i]))
            elif ''.join(textLine[:3]).casefold()  == 'Number2DCells:'.casefold():
                loggedItems.append(('Total 2D Cells', textline[3]))

            elif ''.join(textLine[:4]).casefold()  == '2DDomainCellSizes:'.casefold():
                cellSizes = ''.join(textLine[4:]).split(',')
                for i in range(0, len(cellSizes)):
                    if cellSizes[i]:
                        loggedItems.append(('Cell Size Domain '+str(i+1), cellSizes[i]))



            elif ''.join(textLine[:5]).casefold() in ['ClosingTimeofStartupSummary...'.casefold()]:
                loggedItems.append(('Initialisation Clock Time',cputime))
                loggedItems.append(('Initialisation CPU Time',clocktime))

        except:
            pass

    loggedItems.append(('Final 2D Simulated Time',time))
    loggedItems.append(('Time of last TUFLOW maximum',mxTime))
    return loggedItems
