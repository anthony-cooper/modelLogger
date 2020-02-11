import os.path as path #Used for path commands
import pathlib #Used to rseolve relative paths; Requires python 3.4

#0. (Optional) Parse an IEF to generate 1.


#1. Provide a tcf file path
tcfFile = 'FloodModel_~s1~_~e1~.tcf'
tcfPath = r'C:\DevArea\TestModel\Runs'
homePath = r'C:\DevArea\TestModel'
#1a. (Optional)Provide a list of events

#1b. (Optional) Provide a list of scenarios

def tuflowFileAssessment(textFile,homePath):
    loggedItems =[]
    #2. Read in file
    file = open(textFile,"r")
    #3. Split lines into lists using ' ' and tab as delimters
    splitFile =[]
    for line in file:

        splitFile.append(line.split())
    file.close
    #3a. Split file into blocks by assessing IF, ELSE and END as first values
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
                    break
                else:
                    if filePaths != '':
                        filePaths = filePaths + ' ' + str(textLine[j])
                    else:
                        filePaths = filePaths + str(textLine[j])
    for filePath in filePaths.split('|'):
        filePath = resolveFilePath(filePath.strip(),workingFolder,homePath)
        loggedItems.append((fileType,filePath))
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
