import os.path as path #Used for path commands
import pathlib #Used to rseolve relative paths; Requires python 3.4
from datetime import datetime #Used to format date/times
import re #Regular expressions, used for wildcard matching

#(Optional) Parse an IEF to generate 1.


#Provide a tcf file path
tcfFile = 'FloodModel_~s1~_~e1~.tcf'
tcfPath = r'C:\DevArea\TestModel\Runs'
homePath = r'C:\DevArea\TestModel'
#(Optional)Provide a list of events
events=['','hello']
scenarios=[]
bcEvents = []
#(Optional) Provide a list of scenarios

def tuflowFileAssessment(textFile,homePath):
    loggedItems =[]
    #Read in file
    file = open(textFile,"r")
    #Split lines into lists using ' ' and tab as delimters
    splitFile =[]
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

        if re.search('BC.*EVENT.*SOURCE',line,re.IGNORECASE): #Find BC Event Source
            bcEvents.append((line.split()[line.split().index('|')-1],line.split()[line.split().index('|')+1]))
            print(bcEvents)
        splitFile.append(line.split())

    file.close
    #Split file into blocks by assessing IF, ELSE and END as first values
    textBlock = splitFile
    workingFolder=path.dirname(textFile)

    loggedItems.extend(tuflowTextAssessment(textBlock,workingFolder,homePath))
    return loggedItems

def tuflowTextAssessment(textBlock,workingFolder,homePath):
    loggedItems=[]
    #4. Take list of lists (lines split into words) and handle
    for textLine in textBlock:
        try: #Catch errors from short lines, needs to check in order of number of words
            if textLine[0].casefold()  == 'READ'.casefold():
                loggedItems.extend(genLogItem(textLine,workingFolder,homePath))
            elif ''.join(textLine[:3]).casefold() in ['BCControlFile'.casefold(),'GeometryControlFile'.casefold()]:
                extraFile = genLogItem(textLine,workingFolder,homePath)
                loggedItems.extend(extraFile)
                loggedItems.extend(tuflowFileAssessment(path.join(homePath,extraFile[0][1]),homePath))
        except:
            pass
    return loggedItems


def genLogItem(textLine,workingFolder,homePath):
    fileType = ''
    filePaths = ''
    fileNotes = ''
    fileTime = ''
    loggedItems = []
    if textLine[0].casefold()=='READ'.casefold():
        s=1
    else:
        s=0
    for i in range(s,len(textLine)):
        if textLine[i] == '==':
            fileType = ' '.join(textLine[s:i])
            for j in range(i+1,len(textLine)):
                if textLine[j][0] == '!':
                    try: # Used to prevent failure if notes fail to load
                        fileNotes = ' '.join(textLine[j:])
                        fileNotes = fileNotes[1:]
                    except:
                        pass
                    break
                else:
                    if filePaths != '':
                        filePaths = filePaths + ' ' + str(textLine[j])
                    else:
                        filePaths = filePaths + str(textLine[j])
    if '|' in filePaths:
            if textLine[1].casefold() == 'GIS'.casefold():
                fileNotes = '*Read as ' + str(filePaths.count('|')+1) + ' part group.* ' + fileNotes
            elif textLine[1].casefold() == 'Materials'.casefold():
                fileNotes = '*Multiplier of ' + str(filePaths.split('|')[1]) + ' applied.* ' + fileNotes

    fileNotes = fileNotes.strip()
    for filePath in filePaths.split('|'):
        filePath = resolveFilePath(filePath.strip(),workingFolder,homePath)
        try:
            fileTime = str(datetime.fromtimestamp(path.getmtime(path.join(homePath,filePath))).strftime('%d/%m/%Y %H:%M:%S'))
        except:
            fileTime = 'File Missing'
        loggedItems.append((fileType,filePath,fileNotes,fileTime))
        if not textLine[1].casefold() == 'GIS'.casefold(): # Only read multiple items for GIS files
            break
    return loggedItems


def resolveFilePath(filePath,workingFolder,homePath):
    if not path.isabs(filePath):
        filePath = path.join(workingFolder +'\\'+ filePath)
        filePath = pathlib.Path(filePath).resolve()
    filePath = path.relpath(filePath, start = homePath)
    return filePath

loggedItems = tuflowFileAssessment(path.join(tcfPath,tcfFile),homePath)
for loggedItem in loggedItems:
     print(loggedItem)
