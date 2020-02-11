import os #Used for path commands

#0. (Optional) Parse an IEF to generate 1.


#1. Provide a tcf file path
tcfFile = 'FloodModel_~s1~_~e1~.tcf'
tcfPath = r'C:\DevArea\TestModel\Runs'
homePath = r'C:\DevArea'
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
    workingFolder=os.path.dirname(textFile)

    loggedItems.extend(tuflowTextAssessment(textBlock,workingFolder,homePath))
    for loggedItem in loggedItems:
        print(loggedItem)

def tuflowTextAssessment(textBlock,workingFolder,homePath):
    loggedItems=[]
    #4. Take list of lists (lines split into words) and handle
    for textLine in textBlock:
        if textLine:
            if textLine[0].casefold()  == 'READ'.casefold():
                loggedItems.append(genLogItem(textLine,workingFolder,homePath))
    return loggedItems


def genLogItem(textLine,workingFolder,homePath):
    fileType = ''
    filePath = ''
    for i in range(1,len(textLine)):
        if textLine[i] == '==':
            fileType = ' '.join(textLine[1:i])
            for j in range(i+1,len(textLine)):
                if textLine[j][0] == '!':
                    break
                else:
                    if filePath != '':
                        filePath = filePath + ' ' + str(textLine[j])
                    else:
                        filePath = filePath + str(textLine[j])
            filePath = os.path.join(workingFolder + filePath)
            filePath = os.path.abspath(os.path.realpath(filePath))
            filePath = os.path.relpath(filePath, start = homePath)
    return (fileType,filePath)

tuflowFileAssessment(os.path.join(tcfPath,tcfFile),homePath)
