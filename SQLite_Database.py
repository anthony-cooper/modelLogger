import sqlite3
import os

modelName = 'floodModel'
dbLoc = r'C:\DevArea\TestDB'

#Lists containing tuples containing field Names and Types
modelTableFields = []
modelTableFields.append(('mId','INT AUTO_INCREMENT PRIMARY KEY'))
# Absolute Home path
# Model type
# Submission date
# Signed off
# Sign off date
# Modeller
# Checker
# Approver

simulationTableFields = []
simulationTableFields.append(('sId','INT AUTO_INCREMENT PRIMARY KEY'))
# simulation info (fail?, time, event, scenario, etc)


fileTableFields = []
fileTableFields.append(('fId','INT AUTO_INCREMENT PRIMARY KEY'))
# fileName
# fileExt
# Type
# rel path from home
# modifiers applied
# file last modified
# file exists

commentTableFields = []
commentTableFields.append(('cId','INT AUTO_INCREMENT PRIMARY KEY'))                         #table primary key
commentTableFields.append(('user','VARCHAR(255)'))                                          #User name of commenter
commentTableFields.append(('commentTime','TIMESTAMP'))                                      #Time of comment
commentTableFields.append(('commentText','TEXT'))                                           #Comment Text
commentTableFields.append(('commentType','INT'))                                            #Comment type (question etc)
commentTableFields.append(('threadClosed','INT'))                                           #Mark as a thread closed/signed off
commentTableFields.append(('proceedingComment','INT'))                                      #Previous comment - foreign key link
commentTableFields.append(('succeedingComment','INT'))                                      #Next comment - foreign key link
commentTableFields.append(('FOREIGN KEY(proceedingComment)','REFERENCES comments(cId)'))    #Set up foreign key reference
commentTableFields.append(('FOREIGN KEY(succeedingComment)','REFERENCES comments(cId)'))    #Set up foreign key reference

#Link Tables
model_simulation_LinksFields = []
model_simulation_LinksFields.append(('modelID','INT'))                                                #Model ID - foreign key link
model_simulation_LinksFields.append(('simulationID','INT'))                                           #Simulation ID - foreign key link
model_simulation_LinksFields.append(('FOREIGN KEY(modelID)','REFERENCES models(mId)'))                #Set up foreign key reference
model_simulation_LinksFields.append(('FOREIGN KEY (simulationID)','REFERENCES simulations (sId)')) #Set up foreign key reference

simulation_file_LinksFields = []
simulation_file_LinksFields.append(('simulationID','INT'))                                           #Simulation ID - foreign key link
simulation_file_LinksFields.append(('fileID','INT'))                                                 #File ID - foreign key link
simulation_file_LinksFields.append(('FOREIGN KEY(simulationID)','REFERENCES simulations(sId)'))      #Set up foreign key reference
simulation_file_LinksFields.append(('FOREIGN KEY(fileID)','REFERENCES files(fId)'))                  #Set up foreign key reference

file_file_LinksFields = []
file_file_LinksFields.append(('fileAID','INT'))                                                 #File A ID - foreign key link
file_file_LinksFields.append(('fileBID','INT'))                                                 #File B ID - foreign key link
file_file_LinksFields.append(('fileRelationshipType','INT'))                                    #Type of relationship - parent (eg reference) or parts (eg shps)
file_file_LinksFields.append(('FOREIGN KEY(fileAID)','REFERENCES files(fId)'))                  #Set up foreign key reference
file_file_LinksFields.append(('FOREIGN KEY(fileBID)','REFERENCES files(fId)'))                  #Set up foreign key reference

comment_ALL_LinksFields = []
comment_ALL_LinksFields.append(('commentID','INT'))                                              #Comment ID - foreign key link
comment_ALL_LinksFields.append(('modelID','INT'))                                                #Model ID - foreign key link
comment_ALL_LinksFields.append(('simulationID','INT'))                                           #Simulation ID - foreign key link
comment_ALL_LinksFields.append(('fileID','INT'))                                                 #File ID - foreign key link
comment_ALL_LinksFields.append(('FOREIGN KEY(fileID)','REFERENCES files(fId)'))                  #Set up foreign key reference
comment_ALL_LinksFields.append(('FOREIGN KEY(commentID)','REFERENCES comments(cId)'))            #Set up foreign key reference
comment_ALL_LinksFields.append(('FOREIGN KEY(modelID)','REFERENCES models(mId)'))                #Set up foreign key reference
comment_ALL_LinksFields.append(('FOREIGN KEY(simulationID)','REFERENCES simulations(sId)'))      #Set up foreign key reference


#List containing tuples containing table Names and Fields (as lists)
databaseTables = []
databaseTables.append(('models',modelTableFields))
databaseTables.append(('simulations',simulationTableFields))
databaseTables.append(('files',fileTableFields))
databaseTables.append(('comments',commentTableFields))
databaseTables.append(('model_simulation',model_simulation_LinksFields))
databaseTables.append(('simulation_file',simulation_file_LinksFields))
databaseTables.append(('file_file',file_file_LinksFields))
databaseTables.append(('comments_ALL',comment_ALL_LinksFields))



#Connect to database
print('********** DATABASE SET UP **********')
mydb = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
print('Database opened')

mycursor = mydb.cursor()

print('********** TABLES SET UP **********')
for table in databaseTables:
    sqlCommand = 'CREATE TABLE IF NOT EXISTS '+table[0]+'('
    for field in table[1]:
        sqlCommand = sqlCommand + field[0] + ' ' + field[1] + ', '
    sqlCommand = sqlCommand[:-2] #remove final comma space
    sqlCommand = sqlCommand + ');'
    #print(sqlCommand)
    mycursor.execute(sqlCommand)
    print(table[0] + ' exists')
