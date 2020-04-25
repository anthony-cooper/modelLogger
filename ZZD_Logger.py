import os.path as path #Used for path commands
import pathlib #Used to rseolve relative paths; Requires python 3.4
from datetime import datetime #Used to format date/times
import re #Regular expressions, used for wildcard matching


def zzdLogger(zzdFile):
    loggedItems = []
    nonCons =[]
    ass = zzdFileAssessment(zzdFile)
    loggedItems.extend(ass[0])
    nonCons.extend(ass[1])

    return loggedItems, nonCons

def zzdFileAssessment(textFile):
    loggedItems =[]
    nonCons = []
    #Read in file
    file = open(textFile,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:

        fileLines.append(line.split())

    file.close

    workingFolder=path.dirname(textFile)

    ass = zzdTextAssessment(fileLines)
    loggedItems.extend(ass[0])
    nonCons.extend(ass[1])

    return loggedItems, nonCons

def zzdTextAssessment(textBlock):
    loggedItems=[]
    nonCons = []
    finish=''
    #4. Take list of lists (lines split into words) and handle
    text = iter(textBlock)
    for textLine in text:
        try: #Catch errors from short lines, needs to check in order of number of words
            #print(''.join(textLine[2:5]))

            if textLine[0].casefold()  == 'BUILD:'.casefold():
                loggedItems.append(('TUFLOW Build', textLine[1]))
            elif ''.join(textLine[:2]).casefold() == '***Error'.casefold():
                finish = textLine[2]
            elif ''.join(textLine[:2]).casefold() == 'runcompleted'.casefold():
                finish = 'complete'
                while True:
                    try:
                        summary = next(text)
                        if ':' in ' '.join(summary):
                            loggedItems.append((' '.join(summary).split(':')[0],' '.join(summary).split(':')[1]))
                        elif ' '.join(summary) == '******* End mass balance summary *******':
                            break

                    except:
                        break


            elif ''.join(textLine[2:4]).casefold() == 'FloodModeller'.casefold():
                if textLine[4].split('=')[0] == 'VER':
                    loggedItems.append(('Flood Modeller Version',textLine[4].split('=')[1] ))
                    ne = next(text)
                    loggedItems.append(('Flood Modeller Precision',ne[0]))
                    loggedItems.append(('Flood Modeller Version Type',ne[2] ))
                    ne = next(text)
                    loggedItems.append(('Flood Modeller Start Time', ne[5] + ' ' + ne[3]))

            elif ''.join(textLine[:5]).casefold() == 'Poormodelconvergenceattime'.casefold():
                time = textLine[5]
                ne = next(text)
                te = ''.join(ne)
                qratio = float(te.split('=')[2].split('at')[0])
                qratioN = te.split('=')[2].split('at')[1].split('HRATIO')[0]
                hratio = float(te.split('=')[3].split('at')[0])
                hratioN = te.split('=')[3].split('at')[1]
                ne = next(text)
                te = ''.join(ne)
                maxDq = float(te.split('=')[1].split('at')[0])
                maxDqN = te.split('=')[1].split('at')[1].split('MAX')[0]
                maxDh = float(te.split('=')[2].split('at')[0])
                maxDhN = te.split('=')[2].split('at')[1]
                nonCons.append((time,qratio,qratioN,hratio,hratioN,maxDq,maxDqN,maxDh,maxDhN))






            elif ' '.join(textLine) == 'Flood Modeller 1D Solver run parameters modified as follows:':
                while True:
                    try:
                        ne = next(text)
                        if ''.join(ne[:2]) == 'Initialconditions' or ' '.join(ne) == 'Using default initial conditions (from *.dat file)':
                            break
                        elif ne:
                            loggedItems.append(('Flood Modeller Modified Parameter',' '.join(ne)))

                    except:
                        pass

        except:
            pass
    loggedItems.append(('Flood Modeller Final State', finish))

    return loggedItems, nonCons

print(zzdLogger(r'C:\DevArea\TestModel\FM\Results\BROOKSTRAY_[02-00_EP2020-NC]_[TOPO-B-124-5_CHAN-B-1-5_002].zzd')[1])
