import sqlite3
import os




def generate_header():
    html='''<style>
                .grid-container-base {
                  display: grid;
                  grid-template-columns: 200px auto;
                  grid-template-rows: 40px auto;
                  padding: 5px;
                }
                .grid-container-types {
                  display: grid;
                  grid-template-columns: auto;
                  grid-template-rows: auto auto auto;
                  padding: 10px;
                }
                .grid-container-type {
                  border: 1px solid rgba(0, 0, 0, 0.8);
                  display: grid;
                  grid-template-columns: auto ;
                  grid-template-rows: 32px auto;
                }
                .grid-container-fm {
                  padding: 8px;
                  display: grid;
                  grid-template-columns: auto auto auto;
                  grid-template-rows: auto;
                  background-color: rgba(0, 0, 255, 0.3);
                }
                .grid-container-tuf {
                  padding: 8px;
                  display: grid;
                  grid-template-columns: auto auto;
                  grid-template-rows: auto;
                  background-color: rgba(255, 0, 0, 0.3);
                }
                .grid-container-fil {
                  padding: 8px;
                  display: grid;
                  grid-template-columns: auto;
                  grid-template-rows: auto;
                  background-color: rgba(0, 255, 0, 0.3);
                }
                .grid-item {
                  padding: 8px;
                  font-family: Helvetica, sans-serif;
                  font-size: 16px;
                  text-align: left;
                  font-weight: bold;
                }
                .grid-item-edge {
                  padding: 4px;
                  font-family: Helvetica, sans-serif;
                  font-size: 12px;
                  text-align: left;
                }

                .grid-item-tableHeading {
                  padding: 7px;
                  font-family: Helvetica, sans-serif;
                  font-size: 14px;
                  text-align: center;
                  font-weight: bold;
                }


                table {
                  border-collapse: collapse;
                  width: 100%;
                }
                th {
                  padding: 4px;
                  text-align: left;
                  border: 1px solid #ddd;
                  border-bottom: 1px solid #ddd;
                  font-family: Helvetica, sans-serif;
                  font-weight: bold;
                  font-size: 14px;
                  color: rgb(255,255,255);
                  background-color: rgba(0, 0, 0, 0.5);

                }
                td {
                  padding: 2px;
                  text-align: left;
                  border: 1px solid #ddd;
                  border-bottom: 1px solid #ddd;
                  font-family: Helvetica, sans-serif;
                  font-size: 12px;
                }

                tr:nth-child(odd){
                background-color: rgba(255, 255, 255, 0.3);
                }
                tr:hover {
                background-color: #ddd;
                }

            </style>'''

    return html

def generate_base(cursor, sId, mId):
    sqlCommand = '''SELECT simulations.simName
                    FROM simulations
                    WHERE simulations.sId = ?'''

    cursor.execute(sqlCommand,[sId])
    simName=cursor.fetchone()[0]

    sqlCommand = '''SELECT simulations.simName
                    FROM simulations, models, model_simulation
                    WHERE models.mId = ? AND model_simulation.modelID = model_simulation.simulationId'''

    cursor.execute(sqlCommand,[mId])
    data=cursor.fetchall()
    simulations=''
    for item in data:
        if item[0].count('_[') == 2:
            simulations = simulations + '<tr><td>'+item[0].split('_[')[1][:-1]+'</td><td>'+item[0].split('_[')[2][:-1]+'</td></tr>'
        else:
            simulations = simulations + '<tr><td>'+item[0]+'</td></tr>'

    html='''<div class="grid-container-base">
            	<div class="grid-item"></div>
            	<div class="grid-item">Model Log: '''+simName+'''</div>
            	<div><table>
                    <tr><th>Simulations</th></tr>
                    	'''+simulations+'''
                </table></div>
            	<div class="grid-container-types">'''
    html=html+generate_fm(cursor, sId)
    html=html+generate_tuf(cursor, sId)
    html=html+generate_files(cursor, sId)
    html=html+'''</div>
            </div>'''

    return html

def generate_fm(cursor, sId):
    sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                    FROM simulationExtras, simulations
                    WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 0'''

    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    fmDetTable=''
    for item in data:
        fmDetTable = fmDetTable + '<tr><td>'+item[0]+'</td><td>'+item[1]+'</td></tr>'


    sqlCommand = '''SELECT nsParas.parameter
                    FROM nsParas, simulation_nsParas, simulations
                    WHERE simulations.sId = ? and simulation_nsParas.simulationID = simulations.sId and simulation_nsParas.nsParasID = nsParas.nsParasId  and nsParas.software = 0'''

    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    fmModTable=''
    for item in data:
        fmModTable = fmModTable + '<tr><td>'+item[0]+'</td></tr>'





    html='''<div class="grid-container-type">
    			<div class="grid-item">Flood Modeller Details</div>
    			<div class="grid-container-fm">
    				<div class="grid-container-type">
    					<div class="grid-item-tableHeading">Simulation Details</div>
    					<div><table>
    						<tr><th>Parameter</th><th>Value</th></tr>
    						'''+fmDetTable+'''
    					</table></div>
    				</div>
    				<div class="grid-container-type">
    					<div class="grid-item-tableHeading">Non-default parameters</div>
    					<div><table>
    						<tr><th>Change made</th></tr>
    						'''+fmModTable+'''
    					</table></div>
    				</div>
    				<div class="grid-item">Reserve for FM Plot</div>
    			</div>
    		</div>'''
    return html

def generate_tuf(cursor, sId):
    sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                    FROM simulationExtras, simulations
                    WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 1'''

    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    tufDetTable=''
    for item in data:
        tufDetTable = tufDetTable + '<tr><td>'+item[0]+'</td><td>'+item[1]+'</td></tr>'


    html='''<div class="grid-container-type">
    			<div class="grid-item">TUFLOW Details</div>
    			<div class="grid-container-tuf">
    				<div class="grid-container-type">
    					<div class="grid-item-tableHeading">Simulation Details</div>
    					<div><table>
    						<tr><th>Parameter</th><th>Value</th></tr>
    						'''+tufDetTable+'''
    					</table></div>
    				</div>
    				<div class="grid-item">Reserve for MB plot</div>
    			</div>
    		</div>'''
    return html

def generate_files(cursor, sId):
    sqlCommand = '''SELECT files.fileName, files.fileExt, files.type, files.path, files.readInSettings, files.notes
                    FROM simulation_file, simulations, files
                    WHERE simulations.sId = ? and simulations.sId = simulation_file.simulationID and simulation_file.fileID = files.fId
                    ORDER BY simulations.simName, simulation_file.logOrder'''

    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    filesTable=''
    for item in data:
        notes=''
        if item[4] and item[5]:
            notes = '<p>'+item[4]+'</p><p>'+item[5]+'</p>'
        elif item[4]:
            notes = item[4]
        elif item[5]:
            notes=item[5]
        filesTable = filesTable + '<tr><td>'+item[0]+'</td><td>'+item[1]+'</td><td>'+item[2]+'</td><td>'+item[3]+'</td><td>'+notes+'</td></tr>'


    html='''<div class="grid-container-type">
    			<div class="grid-item">Simulation Files</div>
    			<div class="grid-container-fil">
    					<div><div style="overflow-x:auto;"><table>
    						<tr><th>File Name</th><th>File Extension</th><th>File Type</th><th>File Path</th><th>Read in Settings/Notes</th></tr>
    						'''+filesTable+'''
    					</table></div>
    				</div>
    			</div>
    		</div>'''
    return html

def generate_sim():
    modelName = 'floodModel'
    dbLoc = r'C:\DevArea\TestDB'

    sId = 5
    mId = 1

    #Open Database
    db = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
    cursor = db.cursor()

    html=generate_header()+generate_base(cursor, sId, mId)
    f = open(os.path.join(dbLoc,modelName+'.html'), "w")
    f.write(html)
    f.close()

generate_sim()
