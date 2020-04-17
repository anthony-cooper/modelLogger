import os.path as path #Used for path commands
import pathlib #Used to rseolve relative paths; Requires python 3.4
from datetime import datetime #Used to format date/times
import re #Regular expressions, used for wildcard matching


def tuflowLogger(tcfFile,homePath,events,scenarios):
    loggedItems = []
    fileExists = True

    filePath = resolveFilePath(tcfFile,'',homePath)
    try:
        fileTime = str(datetime.fromtimestamp(path.getmtime(path.join(homePath,filePath))).strftime('%d/%m/%Y %H:%M:%S'))
    except:
        fileExists = False
    fileNotes = ''
    readNotes =''
    loggedItems.append((path.splitext(path.basename(filePath))[0],path.splitext(path.basename(filePath))[1][1:].casefold(),'TUFLOW Control File',filePath,readNotes,fileNotes,fileTime,fileExists,True))

    loggedItems.extend(tuflowFileAssessment(tcfFile,homePath,events,scenarios))

    return loggedItems, events, scenarios

def tuflowFileAssessment(textFile,homePath,events,scenarios):
    loggedItems =[]
    bcEvents =[]
    #Read in file
    file = open(textFile,"r")
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

        if re.search('ESTRY.*CONTROL.*FILE.*AUTO',line,re.IGNORECASE): #Find ECF Auto
            line = re.sub('AUTO',' == '+ str(path.splitext(path.basename(textFile))[0])+'.ecf',line,re.IGNORECASE)

        fileLines.append(line.split())

    file.close
    workingFolder=path.dirname(textFile)

    textBlock = tuflowBlockAssessment(fileLines,events,scenarios) # process the block to remove lines excluded by logic
    #print(textBlock)
    #print('*')
    for line in textBlock:
        # if re.search('BC.*EVENT.*SOURCE',line,re.IGNORECASE): #Find BC Event Source
        #     bcEvents.append((line.split()[line.split().index('|')-1],line.split()[line.split().index('|')+1]))
        try:
            if ''.join(line[:3]).casefold() == 'BCEVENTSOURCE'.casefold():
                bcEvents.append((line[4],line[6]))
        except:
            pass

    loggedItems.extend(tuflowTextAssessment(textBlock,workingFolder,homePath, events, scenarios, bcEvents))

    return loggedItems

def tuflowBlockAssessment(fileLines,events,scenarios):
    #print('START TBA')

    #print(fileLines)
    #print(include)
    loggedItems =[]
    textBlock = []
    ifLines = []
    lowerLevels = []
    level = 0

    check = 1

    for l in range(0,len(fileLines)):
        try:
            #print(str(check) + ': ' +str(level)+': ' + ' '.join(fileLines[l]))

            if check == 1:
                textBlock.append(fileLines[l])
            elif check == 2:
                lowerLevels.append(fileLines[l])

            if fileLines[l][0].casefold() == 'IF'.casefold():
                level = level + 1
                if level == 1:
                    if (fileLines[l][1].casefold() == 'EVENT'.casefold() and fileLines[l][3] in events) or (fileLines[l][1].casefold() == 'SCENARIO'.casefold() and fileLines[l][3] in scenarios):
                            check = 2
                            lowerLevels = []
                    else:
                        check = 0
                    continue


            if fileLines[l][0].casefold() == 'ELSE'.casefold():
                if level == 1:
                    if check == 2: #currently completing an if, ignore rest of block
                        check = -1

                    #elif check == 1: not possible
                    elif check == 0:
                        try:
                            if fileLines[l][1].casefold() == 'IF'.casefold():
                                if level == 1:
                                    if (fileLines[l][2].casefold() == 'EVENT'.casefold() and fileLines[l][4] in events) or (fileLines[l][2].casefold() == 'SCENARIO'.casefold() and fileLines[l][4] in scenarios):
                                            check = 2
                                            lowerLevels = []
                                    else:
                                        check = 0
                                    continue
                        except:
                            check = 2
                            lowerLevels = []

                    #elif check == -1: do nothing, already completed a if/else if




            if ''.join(fileLines[l][:2]).casefold() == 'ENDIF'.casefold():
                level = level - 1
                if level == 0:
                    textBlock.extend(tuflowBlockAssessment(lowerLevels,events,scenarios))
                    lowerLevels = []
                    check = 1

        except:
            pass

    #print('END TBA')
    return textBlock



    # for l in range(0,len(fileLines)):
    #     print(include)
    #     print(fileLines[l])
    #     if include:
    #         textBlock.append(fileLines[l])
    #     try: # Catch Short Lines
    #         if fileLines[l][0].casefold() == 'IF'.casefold():
    #             include = False
    #             ifFail = True
    #
                # if fileLines[l][1].casefold() == 'EVENT'.casefold():
                #     if fileLines[l][3] in events:
                #         include = True
                #         ifFail = False
                #         textBlock.extend(tuflowBlockAssessment(fileLines[l+1:],include,ifFail,events,scenarios))
                #
                #
                # elif fileLines[l][1].casefold() == 'SCENARIO'.casefold():
                #     if fileLines[l][3] in scenarios:
                #         include = True
                #         ifFail = False
                #         textBlock.extend(tuflowBlockAssessment(fileLines[l+1:],include,ifFail,events,scenarios))
    #
    #
    #             break
    #
    #
    #         if fileLines[l][0].casefold() == 'ELSE'.casefold():
    #             print('else')
    #             if ifFail is True:
    #                 try:
    #                     if fileLines[l][1].casefold() == 'IF'.casefold():
    #                         include = False
    #                         ifFail = True
    #
    #                         if fileLines[l][2].casefold() == 'EVENT'.casefold():
    #                             if fileLines[l][4] in events:
    #                                 include = True
    #                                 ifFail = False
    #                                 textBlock.extend(tuflowBlockAssessment(fileLines[l+1:],include,ifFail,events,scenarios))
    #
    #                         elif fileLines[l][2].casefold() == 'SCENARIO'.casefold():
    #                             if fileLines[l][4] in scenarios:
    #                                 include = True
    #                                 ifFail = False
    #                                 textBlock.extend(tuflowBlockAssessment(fileLines[l+1:],include,ifFail,events,scenarios))
    #
    #                         break
    #                     else: #else and somthing not if
    #                         include = True
    #                 except: #just else on the line
    #                     include = True
    #             else:
    #                 print(ifFail)
    #                 include = False
    #
    #
    #         if ''.join(fileLines[l][:2]).casefold() == 'ENDIF'.casefold():
    #             include = True
    #
    #
    #     except:
    #         pass
    # print('FINISH TBA')
    # return textBlock

def tuflowTextAssessment(textBlock,workingFolder,homePath, events, scenarios, bcEvents):
    loggedItems=[]
    #4. Take list of lists (lines split into words) and handle
    for textLine in textBlock:
        try: #Catch errors from short lines, needs to check in order of number of words
            if textLine[0].casefold()  == 'READ'.casefold():
                if textLine[1].casefold()  == 'File'.casefold():
                    extraFile = genLogItem(textLine,workingFolder,homePath)
                    loggedItems.extend(extraFile)
                    loggedItems.extend(tuflowFileAssessment(path.join(homePath,extraFile[0][3]),homePath, events, scenarios))
                else:
                    loggedItems.extend(genLogItem(textLine,workingFolder,homePath))
            elif ''.join(textLine[:2]).casefold() == 'BCDatabase'.casefold():
                extraFile = genLogItem(textLine,workingFolder,homePath)
                loggedItems.extend(extraFile)
                loggedItems.extend(bcTextAssessment(path.join(homePath,extraFile[0][3]), path.dirname(path.join(homePath,extraFile[0][3])),homePath,bcEvents))

            elif ''.join(textLine[:2]).casefold() == 'EventFile'.casefold():
                extraFile = genLogItem(textLine,workingFolder,homePath)
                loggedItems.extend(extraFile)
                loggedItems.extend(tuflowFileAssessment(path.join(homePath,extraFile[0][3]),homePath, events, scenarios))
            elif ''.join(textLine[:2]).casefold() in ['LogFolder'.casefold(),'OutputFolder'.casefold()]:
                extraFile = genLogItem(textLine,workingFolder,homePath)
                loggedItems.extend(extraFile)
                loggedItems.extend(tuflowFileAssessment(path.join(homePath,extraFile[0][3]),homePath, events, scenarios))
            elif ''.join(textLine[:3]).casefold() in ['PitInletDatabase'.casefold(),'DepthDischargeDatabase'.casefold()]:
                extraFile = genLogItem(textLine,workingFolder,homePath)
                loggedItems.extend(extraFile)
                loggedItems.extend(bcTextAssessment(path.join(homePath,extraFile[0][3]), path.dirname(path.join(homePath,extraFile[0][3])),homePath,[]))


            elif ''.join(textLine[:3]).casefold() in ['BCControlFile'.casefold(),'GeometryControlFile'.casefold(),'ESTRYControlFile'.casefold(),'WriteCheckFiles'.casefold()]:
                extraFile = genLogItem(textLine,workingFolder,homePath)
                loggedItems.extend(extraFile)
                loggedItems.extend(tuflowFileAssessment(path.join(homePath,extraFile[0][3]),homePath, events, scenarios))
        except:
            pass
    return loggedItems

def bcTextAssessment(bcFile, workingFolder,homePath,bcEvents):
    loggedItems =[]
    fileExists = True
    #Read in file
    file = open(bcFile,"r")
    next(file) #skip header
    for line in file:
        for event in bcEvents:
            line = re.sub(event[0],event[1],line)
        details = line.split(',')
        filePath = resolveFilePath(details[1],workingFolder,homePath)
        try:
            fileTime = str(datetime.fromtimestamp(path.getmtime(path.join(homePath,filePath))).strftime('%d/%m/%Y %H:%M:%S'))
        except:
            fileExists = False
        fileNotes = '*'+details[3]+' against '+details[2]+' for ' +details[0]+'.*'

        #Notes on modifiers added
        readNotes = ''
        if not details[4] == '':
            readNotes = details[2]+' incremented by '+ details[4]+'.'
        if not details[5] == '':
            readNotes = details[3]+' multiplied by '+ details[5]+'.'
        if not details[6] == '':
            readNotes = details[3]+' incremented by '+ details[6]+'.'
        loggedItems.append((path.splitext(path.basename(filePath))[0],path.splitext(path.basename(filePath))[1][1:].casefold(),'Boundary Curve(s)',filePath,readNotes,fileNotes,fileTime,fileExists, True))

    file.close

    return loggedItems

def genLogItem(textLine,workingFolder,homePath):
    fileType = ''
    filePaths = ''
    fileNotes = ''
    fileTime = ''
    readNotes = ''
    fileExists = True
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

    fileNotes = fileNotes.strip()
    for i, filePath in enumerate(filePaths.split('|')):
        filePath = resolveFilePath(filePath.strip(),workingFolder,homePath)
        fileExists = True
        try:
            fullPath = path.join(homePath,filePath)
            if re.search('.shp',path.splitext(fullPath)[1],re.IGNORECASE):
                modTime = max(path.getmtime(path.splitext(fullPath)[0]+'.shp'),path.getmtime(path.splitext(fullPath)[0]+'.shx'),path.getmtime(path.splitext(fullPath)[0]+'.dbf'))
            elif re.search('.mif',path.splitext(fullPath)[1],re.IGNORECASE):
                modTime = max(path.getmtime(path.splitext(fullPath)[0]+'.mif'),path.getmtime(path.splitext(fullPath)[0]+'.mid'))
            else:
                modTime = path.getmtime(fullPath)

            fileTime = str(datetime.fromtimestamp(modTime).strftime('%d/%m/%Y %H:%M:%S'))
        except:
            fileExists = False

        if '|' in filePaths:
                if textLine[1].casefold() == 'GIS'.casefold():
                    readNotes = 'Read as ' + str(filePaths.count('|')+1) + ' part group with '
                    if len(filePaths.split('|')) == 3:
                        if i == 0:
                            readNotes = readNotes + resolveFilePath(filePaths.split('|')[1].strip(),workingFolder,homePath) + ' and ' + resolveFilePath(filePaths.split('|')[2].strip(),workingFolder,homePath) + '.'
                        elif i == 1:
                            readNotes = readNotes + resolveFilePath(filePaths.split('|')[0].strip(),workingFolder,homePath) + ' and ' + resolveFilePath(filePaths.split('|')[2].strip(),workingFolder,homePath) + '.'
                        else:
                            readNotes = readNotes + resolveFilePath(filePaths.split('|')[0].strip(),workingFolder,homePath) + ' and ' + resolveFilePath(filePaths.split('|')[1].strip(),workingFolder,homePath) + '.'
                    else:
                        readNotes = readNotes + resolveFilePath(filePaths.split('|')[1-i].strip(),workingFolder,homePath) + '.'
                elif textLine[1].casefold() == 'Materials'.casefold():
                    readNotes = 'Multiplier of ' + str(filePaths.split('|')[1]) + ' applied.'

        loggedItems.append((path.splitext(path.basename(filePath))[0],path.splitext(path.basename(filePath))[1][1:].casefold(),fileType,filePath,readNotes,fileNotes,fileTime,fileExists,True))
        if not textLine[1].casefold() == 'GIS'.casefold(): # Only read multiple items for GIS files
            break
    return loggedItems

def resolveFilePath(filePath,workingFolder,homePath):
    if not path.isabs(filePath):
        filePath = path.join(workingFolder +'\\'+ filePath)
    filePath = pathlib.Path(filePath).resolve()
    homePath = pathlib.Path(homePath).resolve()

    filePath = path.relpath(filePath, start = homePath)
    return filePath
