import sqlite3
import os
from TUFLOW_Logger import tuflowLogger
from FloodModeller_Logger import fmLogger
from TLF_Logger import tlfLogger
from ZZD_Logger import zzdLogger
from tuflow_variableLogic import genFileName

modelName = 'floodModel'
dbLoc = r'C:\DevArea\TestDB'

def setup_Database(modelName, dbLoc):
    #Lists containing tuples containing field Names and Types
    modelTableFields = []
    modelTableFields.append(('mId','INT PRIMARY KEY'))
    # Absolute Home path
    # Model type
    # Submission date
    # Signed off
    # Sign off date
    # Modeller
    # Checker
    # Approver

    simulationTableFields = []
    simulationTableFields.append(('sId','INTEGER PRIMARY KEY'))
    simulationTableFields.append(('simName','VARCHAR(255)'))

    # simulation info (fail?, time, event, scenario, etc)


    fileTableFields = []
    fileTableFields.append(('fId','INTEGER PRIMARY KEY'))
    fileTableFields.append(('fileName','VARCHAR(255)'))
    fileTableFields.append(('fileExt','VARCHAR(255)'))
    fileTableFields.append(('type','VARCHAR(255)'))
    fileTableFields.append(('path','VARCHAR(255)'))
    fileTableFields.append(('readInSettings','TEXT'))
    fileTableFields.append(('notes','TEXT'))
    fileTableFields.append(('lastModified','TIMESTAMP'))
    fileTableFields.append(('fileExists','VARCHAR(255)'))


    commentTableFields = []
    commentTableFields.append(('cId','INTEGER PRIMARY KEY'))                         #table primary key
    commentTableFields.append(('user','VARCHAR(255)'))                                          #User name of commenter
    commentTableFields.append(('commentTime','TIMESTAMP'))                                      #Time of comment
    commentTableFields.append(('commentText','TEXT'))                                           #Comment Text
    commentTableFields.append(('commentType','INT'))                                            #Comment type (question etc)
    commentTableFields.append(('threadClosed','INT'))                                           #Mark as a thread closed/signed off
    commentTableFields.append(('proceedingComment','INT'))                                      #Previous comment - foreign key link
    commentTableFields.append(('succeedingComment','INT'))                                      #Next comment - foreign key link
    commentTableFields.append(('FOREIGN KEY(proceedingComment)','REFERENCES comments(cId)'))    #Set up foreign key reference
    commentTableFields.append(('FOREIGN KEY(succeedingComment)','REFERENCES comments(cId)'))    #Set up foreign key reference

    esTableFields = []
    esTableFields.append(('esId','INTEGER PRIMARY KEY'))                      #table primary key
    esTableFields.append(('value','VARCHAR(255)'))                            #Scenario/event
    esTableFields.append(('type','INT'))                                      #event (true), scenario(false)

    nsParasTableFields = []
    nsParasTableFields.append(('nsParasId','INTEGER PRIMARY KEY'))                      #table primary key
    nsParasTableFields.append(('parameter','TEXT'))                            #parameter and change
    nsParasTableFields.append(('software','INT'))                                      #tuflow(true), flood modeller (false)



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

    simulation_es_LinksFields = []
    simulation_es_LinksFields.append(('simulationID','INT'))                                           #Simulation ID - foreign key link
    simulation_es_LinksFields.append(('esID','INT'))                                                 #File ID - foreign key link
    simulation_es_LinksFields.append(('FOREIGN KEY(simulationID)','REFERENCES simulations(sId)'))      #Set up foreign key reference
    simulation_es_LinksFields.append(('FOREIGN KEY(esID)','REFERENCES es(esId)'))                  #Set up foreign key reference

    simulation_nsParas_LinksFields = []
    simulation_nsParas_LinksFields.append(('simulationID','INT'))                                           #Simulation ID - foreign key link
    simulation_nsParas_LinksFields.append(('nsParasID','INT'))                                                 #File ID - foreign key link
    simulation_nsParas_LinksFields.append(('FOREIGN KEY(simulationID)','REFERENCES simulations(sId)'))      #Set up foreign key reference
    simulation_nsParas_LinksFields.append(('FOREIGN KEY(nsParasID)','REFERENCES nsParas(nsParasId)'))                  #Set up foreign key reference

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
    databaseTables.append(('es',esTableFields))
    databaseTables.append(('simulation_es',simulation_es_LinksFields))
    databaseTables.append(('nsParas',nsParasTableFields))
    databaseTables.append(('simulation_nsParas',simulation_nsParas_LinksFields))








    #Connect to database
    print('********** DATABASE Initialisation **********')
    mydb = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
    print('Database opened')

    mycursor = mydb.cursor()

    print('********** TABLES SET UP **********')
    print('*doesn\'t check that tables exist in latest form')
    for table in databaseTables:
        sqlCommand = 'CREATE TABLE IF NOT EXISTS '+table[0]+'('
        for field in table[1]:
            sqlCommand = sqlCommand + field[0] + ' ' + field[1] + ', '
        sqlCommand = sqlCommand[:-2] #remove final comma space
        sqlCommand = sqlCommand + ');'
        #print(sqlCommand)
        mycursor.execute(sqlCommand)
        print(table[0] + ' exists')

    return mydb


def log_sim(db, sim):
    cursor = db.cursor()
    #sqlCommand = 'SELECT fId FROM files WHERE fileName  = ? AND fileExt = ? AND type = ? AND path = ? AND readInSettings = ? AND notes = ?'
    #cursor.execute(sqlCommand,file[:6])
    #data=cursor.fetchone()
    #if data is None:
    if True:
        sqlCommand = 'INSERT INTO simulations(simName) VALUES (?)'
        cursor.execute(sqlCommand, sim)
        db.commit()
        return cursor.lastrowid
    #else:
        #return data[0]
def log_file(db, file):
    cursor = db.cursor()
    sqlCommand = 'SELECT fId FROM files WHERE fileName  = ? AND fileExt = ? AND type = ? AND path = ? AND readInSettings = ? AND notes = ?'
    cursor.execute(sqlCommand,file[:6])
    data=cursor.fetchone()
    if data is None:
        sqlCommand = 'INSERT INTO files(fileName,fileExt,type,path,readInSettings,notes,lastModified,fileExists) VALUES (?,?,?,?,?,?,?,?)'
        cursor.execute(sqlCommand, file)
        db.commit()
        return cursor.lastrowid
    else:
        return data[0]

def link_sim_file(db, sId, fId):
    cursor = db.cursor()
    sqlCommand = 'INSERT INTO simulation_file(simulationID,fileID) VALUES (?,?)'
    cursor.execute(sqlCommand,[sId,fId])
    db.commit()

def log_es(db, value, type):
    cursor = db.cursor()
    sqlCommand = 'SELECT esId FROM es WHERE value  = ? AND type = ?'
    cursor.execute(sqlCommand,[value, type])
    data=cursor.fetchone()
    if data is None:
        sqlCommand = 'INSERT INTO es(value, type) VALUES (?,?)'
        cursor.execute(sqlCommand, [value, type])
        db.commit()
        return cursor.lastrowid
    else:
        return data[0]

def link_sim_es(db, sId, esId):
    cursor = db.cursor()
    sqlCommand = 'INSERT INTO simulation_es(simulationID,esID) VALUES (?,?)'
    cursor.execute(sqlCommand,[sId,esId])
    db.commit()

def log_nsParas(db, parameter, software):
    cursor = db.cursor()
    sqlCommand = 'SELECT nsParasId FROM nsParas WHERE parameter  = ? AND software = ?'
    cursor.execute(sqlCommand,[parameter, software])
    data=cursor.fetchone()
    if data is None:
        sqlCommand = 'INSERT INTO nsParas(parameter, software) VALUES (?,?)'
        cursor.execute(sqlCommand, [parameter, software])
        db.commit()
        return cursor.lastrowid
    else:
        return data[0]

def link_sim_nsParas(db, sId, nsParasId):
    cursor = db.cursor()
    sqlCommand = 'INSERT INTO simulation_nsParas(simulationID,nsParasID) VALUES (?,?)'
    cursor.execute(sqlCommand,[sId,nsParasId])
    db.commit()


iefFile = 'FM_Test.ief'
iefPath = r'C:\DevArea\TestModel\FM'
homePath = r'C:\DevArea\TestModel'


db = setup_Database(modelName, dbLoc)
print('********** SET UP COMPLETE**********')

for file in os.listdir(iefPath):
    if os.path.splitext(file)[1].casefold() == '.ief'.casefold():
        inputs = fmLogger(os.path.join(iefPath,file),homePath)
        simFiles = []
        zzdPath = ''
        tlfFolderPath = ''
        tuflowSimulationName = ''
        sId = log_sim(db,['test'])

        for event in inputs[1]:
            if event:
                esId = log_es(db, event,True)
                link_sim_es(db,sId,esId)
        for scenario in inputs[2]:
            if scenario:
                esId = log_es(db, scenario,False)
                link_sim_es(db,sId,esId)




        for inputFile in inputs[0]:
            if inputFile[2] == 'Flood Modeller Results Folder':
                zzdPath = os.path.join(homePath,inputFile[3]+'.zzd')
            elif inputFile[2] == 'Log Folder':
                tlfFolderPath = os.path.join(homePath,inputFile[3])
            elif inputFile[2] == 'TUFLOW Control File':
                tuflowSimulationName = genFileName(inputFile[0],inputs[1],inputs[2])
                fId = log_file(db,inputFile)
                if fId not in simFiles:
                    link_sim_file(db,sId,fId)
                    simFiles.append(log_file(db,inputFile))

            elif inputFile[2] in ['Output Folder', 'Write Check Files']:
                print(inputFile[3])
            else:
                fId = log_file(db,inputFile)
                if fId not in simFiles:
                    link_sim_file(db,sId,fId)
                    simFiles.append(log_file(db,inputFile))

        print(zzdPath)
        print(os.path.join(tlfFolderPath,tuflowSimulationName+'.tlf'))

        #if being added to simulation tables
            #check if column exists
                #add column if not
            #modify column in existing record (sID) to have given value
        #if flood modeller mod parameter
            #nsParasId = log_nsParas(db, parameter,False)
            #link_sim_nsParas(db,sId,nsParasId)
