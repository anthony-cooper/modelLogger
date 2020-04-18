import sqlite3
import os




def generate_header():
    html='''<html>
<head>

    <style>
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
				.chartDiv-TUFmb {
                    border: 1px solid #ddd;
                    backgroundColor: 'white';
					max-width: 600px;
					max-height: 300px;
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

            </style>


            '''

    return html

def generate_content(cursor, mId):
    sqlCommand = '''SELECT simulations.sId, simulations.simName
                    FROM simulations, models, model_simulation
                    WHERE models.mId = ? AND model_simulation.modelID = model_simulation.simulationId'''

    cursor.execute(sqlCommand,[mId])
    data=cursor.fetchall()
    data = data[0:1]


    simulations=''
    content=''
    script='''
    <script>'''

    for item in data:
        if item[1].count('_[') == 2:
            simulations = simulations + '''<tr id="row'''+str(item[0])+'''" onclick="show'''+str(item[0])+'''()"><td nowrap>'''+item[1].split('_[')[1][:-1]+'''</td><td>'''+item[1].split('_[')[2][:-1]+'''</td nowrap></tr>'''
        else:
            simulations = simulations + '''<tr id="row'''+str(item[0])+'''" onclick="show'''+str(item[0])+'''()"><td nowrap>'''+item[1]+'''</td></tr>'''

        sqlCommand = '''SELECT simulations.simName
                        FROM simulations
                        WHERE simulations.sId = ?'''

        cursor.execute(sqlCommand,[item[0]])
        simName=cursor.fetchone()[0]

        content=content+generate_base(cursor, item[0])

        script =script+'''function show'''+str(item[0])+'''() {
                    '''

        for itemX in data:
            if itemX[0] == item[0]:
                script = script+'''document.getElementById("'''+str(itemX[0])+'''").style.display = "inherit";
                    document.getElementById("row'''+str(itemX[0])+'''").style.color = "rgb(255, 255, 255)";
                    document.getElementById("row'''+str(itemX[0])+'''").style.backgroundColor = "rgb(0, 0, 0)";
                    document.getElementById("row'''+str(itemX[0])+'''").style.fontWeight = "bold";

                    '''
            else:
                script = script+'''document.getElementById("'''+str(itemX[0])+'''").style.display = "none";
                    document.getElementById("row'''+str(itemX[0])+'''").style.color = "inherit";
                    document.getElementById("row'''+str(itemX[0])+'''").style.backgroundColor = "inherit";
                    document.getElementById("row'''+str(itemX[0])+'''").style.fontWeight = "inherit";

                    '''


        script=script+'''document.getElementById("simTitle").innerHTML = "Model Log: '''+simName+'''"}
                '''



    script = script+'''
        </script>'''


    script=script + '''
        <script>
            window.onload = function show() {
                '''
    script=script+'''show'''+str(data[0][0])+'''()
            }
        </script>

</head>'''

    html='''<div class="grid-container-base">
            	<div class="grid-item"></div>
            	<div class="grid-item" id="simTitle">Model Log: Simulation Name</div>
            	<div><table>
                    <tr><th colspan="2">Simulations</th></tr>
                    	'''+simulations+'''
                </table></div>

            '''
    html=script+'''

    '''+html+content
    html=html+'''</div>


'''


    script='''<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js"></script>
    <script>'''


    for item in data:
        sqlCommand = '''SELECT TUFmb.time, TUFmb.CumQME
                        FROM TUFmb
                        WHERE TUFmb.simulationId = ?
                        ORDER BY TUFmb.time'''
        cursor.execute(sqlCommand,[item[0]])
        data=cursor.fetchall()
        tdata = list(zip(*data))
        if not tdata:
            tdata = [[0],[0]]

        #print(', '.join(map(str,tdata[1])))

        script = script +'''var TUFChart'''+str(item[0])+''' = new Chart(document.getElementById('TUFChart'''+str(item[0])+''''), {
        type: 'line',
        data: {
            labels: ['''+', '.join(map(str,tdata[0]))+'''],
            datasets: [
                {
                label: 'Cum. Q ME',
                fill: false,
                pointRadius: 0,
                borderColor: 'orange',
                data: ['''+', '.join(map(str,tdata[1]))+''']
                }
            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            legend: {
                display: true,
                position: 'right',
            },
            scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Time'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: '%'
						}
					}]
				}
        }
});
'''

        sqlCommand = '''SELECT FMlf.time, FMlf.flowCon, FMlf.qtol, FMlf.levelCon, FMlf.htol, FMlf.maxitr, FMlf.minitr, FMlf.iterations, FMlf.massError
                        FROM FMlf
                        WHERE FMlf.simulationId = ?
                        ORDER BY FMlf.time'''
        cursor.execute(sqlCommand,[item[0]])
        data=cursor.fetchall()
        tdata = list(zip(*data))
        if not tdata:
            tdata = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]

        #print(', '.join(map(str,tdata[1])))

        script = script +'''var FMConChart'''+str(item[0])+''' = new Chart(document.getElementById('FMConChart'''+str(item[0])+''''), {
        type: 'line',
        data: {
            labels: ['''+', '.join(map(str,tdata[0]))+'''],
            datasets: [
                {
                label: 'Flow Convergence',
                fill: false,
                pointRadius: 0,
                borderColor: 'red',
                data: ['''+', '.join(map(str,tdata[1]))+''']
                },
                {
                label: 'Flow Tolerance',
                fill: false,
                pointRadius: 0,
                borderColor: 'red',
                borderDash: [5,5],
                borderDashOffset: 0,


                data: ['''+', '.join(map(str,tdata[2]))+''']
                },
                {
                label: 'Level Convergence',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',

                data: ['''+', '.join(map(str,tdata[3]))+''']
                },
                {
                label: 'Level Tolerance',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',
                borderDash: [5,5],
                borderDashOffset: 5,

                data: ['''+', '.join(map(str,tdata[4]))+''']
                }

            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            tooltips: {
                mode: 'index'
            },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0
                }
            },

            legend: {
                display: true,
                position: 'bottom',
                labels: {
                    fontSize: 10,
                    fontColor: 'black',
                    padding: 4
                }
            },
            scales: {
					xAxes: [{
						display: true,
                        maxRotation: 0,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                            padding: 2
                        },
						scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
                            padding: 2
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                            padding: 2
                        },

						scaleLabel: {
							display: false,
						}
					}]
				}
        }
});
'''


    script=script+'''</script>'''

    html=html+script+'''</html>'''
    return html

def generate_base(cursor, sId):



    html='''    <div class="grid-container-types" id="'''+str(sId)+'''">
            '''

    html=html+generate_fm(cursor, sId)
    html=html+generate_tuf(cursor, sId)
    html=html+generate_files(cursor, sId)
    html=html+'''   </div>
            '''

    return html

def generate_fm(cursor, sId):
    sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                    FROM simulationExtras, simulations
                    WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 0'''

    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    fmDetTable=''
    for item in data:
        fmDetTable = fmDetTable + '''<tr><td>'''+item[0]+'''</td><td>'''+item[1]+'''</td></tr>
                                    '''


    sqlCommand = '''SELECT nsParas.parameter
                    FROM nsParas, simulation_nsParas, simulations
                    WHERE simulations.sId = ? and simulation_nsParas.simulationID = simulations.sId and simulation_nsParas.nsParasID = nsParas.nsParasId  and nsParas.software = 0'''

    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    fmModTable=''
    for item in data:
        fmModTable = fmModTable + '''<tr><td>'''+item[0]+'''</td></tr>
                                    '''





    html='''        <div class="grid-container-type">
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
            				<div class="chartDiv-TUFmb" ><canvas id="FMConChart'''+str(sId)+'''"style="width:100%;height:100%;"></canvas></div>
            			</div>
            		</div>
            '''
    return html

def generate_tuf(cursor, sId):
    sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                    FROM simulationExtras, simulations
                    WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 1'''

    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    tufDetTable=''
    for item in data:
        tufDetTable = tufDetTable + '''<tr><td>'''+item[0]+'''</td><td>'''+item[1]+'''</td></tr>
                                    '''


    html='''        <div class="grid-container-type">
            			<div class="grid-item">TUFLOW Details</div>
            			<div class="grid-container-tuf">
            				<div class="grid-container-type">
            					<div class="grid-item-tableHeading">Simulation Details</div>
            					<div><table>
            						<tr><th>Parameter</th><th>Value</th></tr>
            						'''+tufDetTable+'''
            					</table></div>
            				</div>
            				<div class="chartDiv-TUFmb" ><canvas id="TUFChart'''+str(sId)+'''"style="width:100%;height:100%;"></canvas></div>
            			</div>
            		</div>
            '''
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
        filesTable = filesTable + '''<tr><td>'''+item[0]+'''</td><td>'''+item[1]+'''</td><td>'''+item[2]+'''</td><td>'''+item[3]+'''</td><td>'''+notes+'''</td></tr>
                                    '''


    html='''        <div class="grid-container-type">
            			<div class="grid-item">Simulation Files</div>
            			<div class="grid-container-fil">
            					<div><table>
            						<tr><th>File Name</th><th>File Extension</th><th>File Type</th><th>File Path</th><th>Read in Settings/Notes</th></tr>
            						'''+filesTable+'''
            					</table></div>
            			</div>
            		</div>
            '''
    return html

def generate_log():
    modelName = 'reptonStreet'
    dbLoc = r'C:\DevArea\TestDB'

    sId = 5
    mId = 1

    #Open Database
    db = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
    cursor = db.cursor()

    html=generate_header()+generate_content(cursor, mId)
    f = open(os.path.join(dbLoc,modelName+'.html'), "w")
    f.write(html)
    f.close()

generate_log()
# modelName = 'floodModel'
# dbLoc = r'C:\DevArea\TestDB'
#
# db = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
# cursor = db.cursor()
# sId = 1
# genTUFmbPlot(cursor, sId)
