import os.path as path #Used for path commands
import pathlib #Used to rseolve relative paths; Requires python 3.4
from datetime import datetime #Used to format date/times
import re #Regular expressions, used for wildcard matching
from TUFLOW_Logger import tuflowLogger


def fmLogger(iefFile,homePath):
    loggedItems = []

    filePath = resolveFilePath(iefFile,'',homePath)
    try:
        fileTime = str(datetime.fromtimestamp(path.getmtime(path.join(homePath,filePath))).strftime('%d/%m/%Y %H:%M:%S'))
    except:
        fileTime = 'File Missing'
    fileNotes = ''
    loggedItems.append(('Flood Modeller Event File',filePath,fileNotes,fileTime))

    loggedItems.extend(fmFileAssessment(iefFile,homePath))

    return loggedItems

def fmFileAssessment(textFile,homePath):
    loggedItems =[]
    #Read in file
    file = open(textFile,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:
        fileLines.append(line.split('='))
    file.close

    workingFolder=path.dirname(textFile)

    loggedItems.extend(fmTextAssessment(fileLines,workingFolder,homePath))

    return loggedItems

def fmTextAssessment(textBlock,workingFolder,homePath):
    loggedItems=[]
    events = []
    scenarios = []
    tcf = ''


    #4. Take list of lists (lines split into words) and handle
    for textLine in textBlock:
        try: #Catch errors from short lines, needs to check in order of number of words
            if textLine[0].casefold()  == 'Datafile'.casefold():
                loggedItems.extend(genLogItem(textLine[1], 'Flood Modeller Network Data',workingFolder,homePath))
            elif textLine[0].casefold()  == 'InitialConditions'.casefold():
                loggedItems.extend(genLogItem(textLine[1],'Flood Modeller Initial Conditions',workingFolder,homePath))
            elif textLine[0].casefold()  == 'EventData'.casefold():
                loggedItems.extend(genLogItem(textLine[1],'Flood Modeller Event Data', workingFolder,homePath))
            elif textLine[0].casefold()  == '2DFile'.casefold():
                tcf = textLine[1].strip()
            elif textLine[0].casefold()  == '2DOptions'.casefold():
                opts = textLine[1].split()
                for i in range(0, len(opts)):
                    try:
                        if opts[i][0] == '-':
                            try:
                                if opts[i][1] == 'e':
                                    try:
                                        while len(events) < int(opts[i][2])+1:
                                            events.append('')
                                        events[int(opts[i][2])] = opts[i+1]
                                    except:
                                        events = [opts[i+1]]
                                elif opts[i][1] == 's':
                                    try:
                                        while len(scenarios) < int(opts[i][2])+1:
                                            scenarios.append('')
                                        scenarios[int(opts[i][2])] = opts[i+1]
                                    except:
                                        scenarios = [opts[i+1]]
                            except: pass
                    except: pass
        except:
            pass

    if tcf != '':
        if not path.isabs(tcf):
            tcf = path.join(workingFolder +'\\'+ tcf)
            tcf = pathlib.Path(tcf).resolve()
        try:
            loggedItems.extend(tuflowLogger(tcf,homePath,events,scenarios))
        except:
            loggedItems.append(('TUFLOW Control File',resolveFilePath(tcf,workingFolder,homePath),'','File Missing'))

    return loggedItems



def genLogItem(file, fileType,workingFolder,homePath):
    fileNotes = ''
    fileTime = ''
    loggedItems = []

    filePath = resolveFilePath(file.strip(),workingFolder,homePath)
    try:
        fullPath = path.join(homePath,filePath)
        modTime = path.getmtime(fullPath)
        fileTime = str(datetime.fromtimestamp(modTime).strftime('%d/%m/%Y %H:%M:%S'))
    except:
        fileTime = 'File Missing'
    loggedItems.append((fileType,filePath,fileNotes,fileTime))
    return loggedItems

def resolveFilePath(filePath,workingFolder,homePath):
    if not path.isabs(filePath):
        filePath = path.join(workingFolder +'\\'+ filePath)
        filePath = pathlib.Path(filePath).resolve()
    filePath = path.relpath(filePath, start = homePath)
    return filePath
