import os #Used for listing files in folder
import os.path as path #Used for path commands
import SQLite_Database
import html_ReportCreator
import datetime


#Key Parameters
modelName = 'Model'
dbLoc = r'C:\DevArea\TestDB'
modelType = 2

#Model Details
versionName = '001'
versionNotes = 'Check model'
submissionDate = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
modeller = 'Anthony Cooper'
homePath = dbLoc
modelDetails = [versionName,versionNotes,submissionDate,modelType,modeller,homePath]

#Generate list of simulations to include
simsToLog = []

#Single IEF
simsToLog.append([r'C:\DevArea\TestModel\FM\IEF\FM_Test.ief'])


#All IEFs in a Folder
# iefPath = r'\FloodModeller\IEF'
# for file in os.listdir(iefPath):
#     if os.path.splitext(file)[1].casefold() == '.ief'.casefold():
#         simsToLog.append([os.path.join(iefPath,file)])

#TCFs - specify event/simulations
# tcfPath = r'TUFLOW\Model_[~e1~_~e2~]_[~s1~_~s2~_001].tcf'
# simsToLog.append([tcfPath,['','01-00','EP2120-CE'],['','S','_']])
# simsToLog.append([tcfPath,['','01-00','EP2120-CE'],['','S','_']])



mId = SQLite_Database.create_update_Database(modelName, dbLoc, modelType, modelDetails, simsToLog)
print('*************************************************')

print('********** SIMULATION LOGGING COMPLETE **********')
html_ReportCreator.generate_log(modelName, dbLoc, modelType, mId)
