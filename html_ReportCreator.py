import sqlite3
import os
modelName = 'floodModel'
dbLoc = r'C:\DevArea\TestDB'

sId = 5

#Open Database
db = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
cursor = db.cursor()

#Get all files for a simulation
sqlCommand = '''SELECT files.fileName, files.fileExt, files.type, files.path, files.readInSettings, files.notes
                FROM simulation_file, simulations, files
                WHERE simulations.sId = ? and simulations.sId = simulation_file.simulationID and simulation_file.fileID = files.fId
                ORDER BY simulations.simName, simulation_file.logOrder'''

cursor.execute(sqlCommand,[sId])
data=cursor.fetchall()
print(data)

#Get TUFLOW details for a simulation
sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                FROM simulationExtras, simulations
                WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 1'''

cursor.execute(sqlCommand,[sId])
data=cursor.fetchall()
print(data)

#Get Flood Modeller details for a simulation
sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                FROM simulationExtras, simulations
                WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 0'''

cursor.execute(sqlCommand,[sId])
data=cursor.fetchall()
print(data)

#Get Flood Modeller non-defaults for a simulation
sqlCommand = '''SELECT nsParas.parameter
                FROM nsParas, simulation_nsParas, simulations
                WHERE simulations.sId = ? and simulation_nsParas.simulationID = simulations.sId and simulation_nsParas.nsParasID = nsParas.nsParasId  and nsParas.software = 0'''

cursor.execute(sqlCommand,[sId])
data=cursor.fetchall()
print(data)



#Create summary sheet

#For each simulation in model
#Create new sheet
