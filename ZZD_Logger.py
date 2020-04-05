import os.path as path #Used for path commands
import pathlib #Used to rseolve relative paths; Requires python 3.4
from datetime import datetime #Used to format date/times
import re #Regular expressions, used for wildcard matching


def zzdLogger(zzdFile):
    loggedItems = []
    loggedItems.extend(zzdFileAssessment(zzdFile))

    return loggedItems

def zzdFileAssessment(textFile):
    loggedItems =[]
    #Read in file
    file = open(textFile,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:

        fileLines.append(line.split())

    file.close

    workingFolder=path.dirname(textFile)

    loggedItems.extend(zzdTextAssessment(fileLines))

    return loggedItems

def zzdTextAssessment(textBlock):
    loggedItems=[]
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

            elif ' '.join(textLine) == 'Flood Modeller 1D Solver run parameters modified as follows:':
                while True:
                    try:
                        ne = next(text)
                        if ''.join(ne[:2]) == 'Initialconditions':
                            break
                        elif ne:
                            loggedItems.append(('Flood Modeller Modified Parameter',' '.join(ne)))

                    except:
                        pass

        except:
            pass
    loggedItems.append(('Flood Modeller Final State', finish))

    return loggedItems
