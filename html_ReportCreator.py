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
                  grid-template-columns: 33% 33% 34%;
                  grid-template-rows: auto 400px;
                  background-color: rgba(0, 0, 255, 0.3);
                }
                .grid-container-tuf {
                  padding: 8px;
                  display: grid;
                  grid-template-columns: 50% 50%;
                  grid-template-rows: auto;
                  background-color: rgba(255, 0, 0, 0.3);
                }
                .grid-container-tufPlots {
                  display: grid;
                  grid-template-columns: auto;
                  grid-template-rows: 50% 50%;
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
                  border: 1px solid rgba(0, 0, 0, 0.8);
                    background-color: rgba(255, 255, 255, 0.6);
					min-width: 400px;
                    width: 100%;
					min-height: 400px;
                    height: 100%
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
    data = data[0:1] # Only do first element


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
        sqlCommand = '''SELECT TUFmb.time, TUFmb.CumQME, TUFmb.HVolIn, TUFmb.HVolOut, TUFmb.QVolIn, TUFmb.QVolOut, TUFmb.TotVolIn, TUFmb.TotVolOut
                        FROM TUFmb
                        WHERE TUFmb.simulationId = ?
                        ORDER BY TUFmb.time'''
        cursor.execute(sqlCommand,[item[0]])
        data=cursor.fetchall()
        tdata = list(zip(*data))
        if not tdata:
            tdata = [[0],[0],[0],[0],[0],[0],[0],[0]]

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
                borderColor: 'purple',
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[1]))+''']
                }
            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            title: {
					display: true,
					text: 'TUFLOW Mass Balance'
				},
            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: '%',
                            fontSize: 10,
                            fontColor: 'black',

						}
					}]
				}
        }
});
'''

        script = script +'''var TUFVolChart'''+str(item[0])+''' = new Chart(document.getElementById('TUFVolChart'''+str(item[0])+''''), {
        type: 'line',
        data: {
            labels: ['''+', '.join(map(str,tdata[0]))+'''],
            datasets: [
                {
                label: 'Vol. In (Stage Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'brown',
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[2]))+''']
                },
                {
                label: 'Vol. Out (Stage Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'hotpink',
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[3]))+''']
                },
                {
                label: 'Vol. In (Flow Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'green',
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[4]))+''']
                },
                {
                label: 'Vol. Out (Flow Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'orange',
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[5]))+''']
                },
                {
                label: 'Vol. In (Total)',
                fill: false,
                pointRadius: 0,
                borderColor: 'red',
                borderWidth: 2,
                data: ['''+', '.join(map(str,tdata[6]))+''']
                },
                {
                label: 'Vol. Out (Total)',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',
                borderWidth: 2,
                data: ['''+', '.join(map(str,tdata[7]))+''']
                },
            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            title: {
					display: true,
					text: 'TUFLOW Volumes'
				},
            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Volume (m3)',
                            fontSize: 10,
                            fontColor: 'black',

						}
					}]
				}
        }
});
'''


        sqlCommand = '''SELECT FMlf.time, FMlf.flowCon, FMlf.qtol, FMlf.levelCon, FMlf.htol, FMlf.inflow, FMlf.outflow, FMlf.maxitr, FMlf.minitr, FMlf.iterations, FMlf.massError
                        FROM FMlf
                        WHERE FMlf.simulationId = ?
                        ORDER BY FMlf.time'''
        cursor.execute(sqlCommand,[item[0]])
        data=cursor.fetchall()
        tdata = list(zip(*data))
        if not tdata:
            tdata = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

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
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[1]))+''']
                },
                {
                label: 'Flow Tolerance',
                fill: false,
                pointRadius: 0,
                borderColor: 'red',
                borderDash: [5,5],
                borderDashOffset: 0,
                borderWidth: 1,


                data: ['''+', '.join(map(str,tdata[2]))+''']
                },
                {
                label: 'Level Convergence',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',
                borderWidth: 1,

                data: ['''+', '.join(map(str,tdata[3]))+''']
                },
                {
                label: 'Level Tolerance',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',
                borderDash: [5,5],
                borderDashOffset: 5,
                borderWidth: 1,

                data: ['''+', '.join(map(str,tdata[4]))+''']
                }

            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            title: {
					display: true,
					text: 'FM Convergence'
				},

            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Convergence',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}]
				}
        }
});
'''
        script = script +'''var FMIOChart'''+str(item[0])+''' = new Chart(document.getElementById('FMIOChart'''+str(item[0])+''''), {
        type: 'line',
        data: {
            labels: ['''+', '.join(map(str,tdata[0]))+'''],
            datasets: [
                {
                label: 'Inflow',
                fill: false,
                pointRadius: 0,
                borderColor: 'green',
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[5]))+''']
                },
                {
                label: 'Outflow',
                fill: false,
                pointRadius: 0,
                borderColor: 'orange',
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[6]))+''']
                }
            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            title: {
					display: true,
					text: 'FM Flows'
				},

            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Flow (m3/s)',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}]
				}
        }
});
'''
        script = script +'''var FMItsChart'''+str(item[0])+''' = new Chart(document.getElementById('FMItsChart'''+str(item[0])+''''), {
        type: 'line',
        data: {
            labels: ['''+', '.join(map(str,tdata[0]))+'''],
            datasets: [
                {
                label: 'Max Iterations',
                fill: false,
                pointRadius: 0,
                borderColor: 'black',
                borderDash: [5,5],
                borderWidth: 1,
                data: ['''+', '.join(map(str,tdata[7]))+''']
                },
                {
                label: 'Min Iterations',
                fill: false,
                pointRadius: 0,
                borderColor: 'black',
                borderDash: [5,5],
                borderWidth: 1,

                data: ['''+', '.join(map(str,tdata[8]))+''']
                },
                {
                label: 'Iterations',
                fill: false,
                pointRadius: 0,
                borderColor: 'brown',
                borderWidth: 1,

                data: ['''+', '.join(map(str,tdata[9]))+''']
                }
            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            title: {
					display: true,
					text: 'FM Iterations'
				},

            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: 'Iterations',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}]
				}
        }
});
'''
        script = script +'''var FMMBChart'''+str(item[0])+''' = new Chart(document.getElementById('FMMBChart'''+str(item[0])+''''), {
        type: 'line',
        data: {
            labels: ['''+', '.join(map(str,tdata[0]))+'''],
            datasets: [
                {
                label: '1D Mass Error',
                fill: false,
                pointRadius: 0,
                borderColor: 'hotpink',
                borderWidth: 1,

                data: ['''+', '.join(map(str,tdata[10]))+''']
                }
            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            title: {
					display: true,
					text: 'FM Mass Balance'
				},

            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
	                        gridLines: {
                                drawTicks: false
                            },
					scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: '%',
                            fontSize: 10,
                            fontColor: 'black',
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





    FMhtml='''        <div class="grid-container-type">
            			<div class="grid-item">Flood Modeller Details</div>
            			<div class="grid-container-fm">
            				<div class="grid-container-type">
            					<div class="grid-item-tableHeading">Simulation Details</div>
            					<div><table id="FMDetTable">
            						<tr><th>Parameter</th><th>Value</th></tr>
            					</table></div>
            				</div>
            				<div class="grid-container-type">
            					<div class="grid-item-tableHeading">Non-default parameters</div>
            					<div><tableid="FMModTable">
            						<tr><th>Change made</th></tr>
            					</table></div>
            				</div>
            				<div class="chartDiv-TUFmb" ><canvas id="FMConChart"style="width:100%;height:100%;"></canvas></div>
            				<div class="chartDiv-TUFmb" ><canvas id="FMIOChart"style="width:100%;height:100%;"></canvas></div>
            				<div class="chartDiv-TUFmb" ><canvas id="FMItsChart"style="width:100%;height:100%;"></canvas></div>
            				<div class="chartDiv-TUFmb" ><canvas id="FMMBChart"style="width:100%;height:100%;"></canvas></div>

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
                            <div class="grid-container-tufPlots">
                                <div class="chartDiv-TUFmb" ><canvas id="TUFVolChart'''+str(sId)+'''"style="width:100%;height:100%;"></canvas></div>
            				    <div class="chartDiv-TUFmb" ><canvas id="TUFChart'''+str(sId)+'''"style="width:100%;height:100%;"></canvas></div>
                            </div>
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





def CSS():
    CSS='''
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
      grid-template-columns: 33% 33% 34%;
      grid-template-rows: auto 400px;
      background-color: rgba(0, 0, 255, 0.3);
    }
    .grid-container-tuf {
      padding: 8px;
      display: grid;
      grid-template-columns: 50% 50%;
      grid-template-rows: auto;
      background-color: rgba(255, 0, 0, 0.3);
    }
    .grid-container-tufPlots {
      display: grid;
      grid-template-columns: auto;
      grid-template-rows: 50% 50%;
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
      border: 1px solid rgba(0, 0, 0, 0.8);
        background-color: rgba(255, 255, 255, 0.6);
        min-width: 400px;
        width: 100%;
        min-height: 400px;
        height: 100%
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
    return CSS

def FMhtml():
    FMhtml='''
    <div class="grid-container-type">
    	<div class="grid-item">Flood Modeller Details</div>
    	<div class="grid-container-fm">
    		<div class="grid-container-type">
    			<div class="grid-item-tableHeading">Simulation Details</div>
    			<div><table id="FMDetTable">
    				<tr><th>Parameter</th><th>Value</th></tr>
    			</table></div>
    		</div>
    		<div class="grid-container-type">
    			<div class="grid-item-tableHeading">Non-default parameters</div>
    			<div><table id="FMModTable">
    				<tr><th>Change made</th></tr>
    			</table></div>
    		</div>
    		<div class="chartDiv-TUFmb" ><canvas id="FMConChart"style="width:100%;height:100%;"></canvas></div>
    		<div class="chartDiv-TUFmb" ><canvas id="FMIOChart"style="width:100%;height:100%;"></canvas></div>
    		<div class="chartDiv-TUFmb" ><canvas id="FMItsChart"style="width:100%;height:100%;"></canvas></div>
    		<div class="chartDiv-TUFmb" ><canvas id="FMMBChart"style="width:100%;height:100%;"></canvas></div>

        </div>
    </div>
    '''
    return FMhtml

def TUFhtml():
    TUFhtml='''
    <div class="grid-container-type">
    	<div class="grid-item">TUFLOW Details</div>
    	<div class="grid-container-tuf">
    		<div class="grid-container-type">
    			<div class="grid-item-tableHeading">Simulation Details</div>
    			<div><table id="TUFDetTable">
    				<tr><th>Parameter</th><th>Value</th></tr>
    			</table></div>
    		</div>
            <div class="grid-container-tufPlots">
                <div class="chartDiv-TUFmb" ><canvas id="TUFVolChart"style="width:100%;height:100%;"></canvas></div>
    		    <div class="chartDiv-TUFmb" ><canvas id="TUFMBChart"style="width:100%;height:100%;"></canvas></div>
            </div>
    	</div>
    </div>
    '''
    return TUFhtml

def FILhtml():
    FILhtml='''
    <div class="grid-container-type">
    	<div class="grid-item">Simulation Files</div>
    	<div class="grid-container-fil">
    			<div><table id="filesTable">
    				<tr><th>File Name</th><th>File Extension</th><th>File Type</th><th>File Path</th><th>Read in Settings/Notes</th></tr>
    			</table></div>
    	</div>
    </div>
    '''
    return FILhtml

def FMConChart():
    script='''
    var FMConChart = new Chart(document.getElementById('FMConChart'), {
        type: 'line',
        data: {
            labels: [1,2,3,4],
            datasets: [
                {
                label: 'Flow Convergence',
                fill: false,
                pointRadius: 0,
                borderColor: 'red',
                borderWidth: 1,
                data: [1,2,3,4]
                },
                {
                label: 'Flow Tolerance',
                fill: false,
                pointRadius: 0,
                borderColor: 'red',
                borderDash: [5,5],
                borderDashOffset: 0,
                borderWidth: 1,


                data: [2,4,6,8]
                },
                {
                label: 'Level Convergence',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',
                borderWidth: 1,

                data: [3,6,9,12]
                },
                {
                label: 'Level Tolerance',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',
                borderDash: [5,5],
                borderDashOffset: 5,
                borderWidth: 1,

                data: [4,8,12,16]
                }

            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                    display: true,
                    text: 'FM Convergence'
                },

            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
                        }
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Convergence',
                            fontSize: 10,
                            fontColor: 'black',
                        }
                    }]
                }
        }
    });
    '''
    return script

def FMIOChart():
    script='''
    var FMIOChart = new Chart(document.getElementById('FMIOChart'), {
        type: 'line',
        data: {
            labels: [1,2,3,4],
            datasets: [
                {
                label: 'Inflow',
                fill: false,
                pointRadius: 0,
                borderColor: 'green',
                borderWidth: 1,
                data: [1,2,3,4]
                },
                {
                label: 'Outflow',
                fill: false,
                pointRadius: 0,
                borderColor: 'orange',
                borderWidth: 1,
                data: [2,4,6,8]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                    display: true,
                    text: 'FM Flows'
                },

            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
                        }
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Flow (m3/s)',
                            fontSize: 10,
                            fontColor: 'black',
                        }
                    }]
                }
        }
    });
    '''
    return script

def FMItsChart():
    script='''
var FMItsChart = new Chart(document.getElementById('FMItsChart'), {
    type: 'line',
    data: {
        labels: [1,2,3,4],
        datasets: [
            {
            label: 'Max Iterations',
            fill: false,
            pointRadius: 0,
            borderColor: 'black',
            borderDash: [5,5],
            borderWidth: 1,
            data: [1,2,3,4]
            },
            {
            label: 'Min Iterations',
            fill: false,
            pointRadius: 0,
            borderColor: 'black',
            borderDash: [5,5],
            borderWidth: 1,

            data: [2,4,6,8]
            },
            {
            label: 'Iterations',
            fill: false,
            pointRadius: 0,
            borderColor: 'brown',
            borderWidth: 1,

            data: [3,6,9,12]
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
                display: true,
                text: 'FM Iterations'
            },

        tooltips: {
            mode: 'index',
            intersect: false,
            titleFontSize: 10,
            bodyFontSize: 10,
            displayColors: false
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
                    },
                    gridLines: {
                        drawTicks: false
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Time',
                        fontSize: 10,
                        fontColor: 'black',
                    }
                }],
                yAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true,
                        maxRotation: 0,
                        minRotation: 0,
                        fontSize: 10,
                        fontColor: 'black',
                    },
                    gridLines: {
                        drawTicks: false
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Iterations',
                        fontSize: 10,
                        fontColor: 'black',
                    }
                }]
            }
        }
    });
    '''
    return script

def FMMBChart():
    script = '''
    var FMMBChart = new Chart(document.getElementById('FMMBChart'), {
        type: 'line',
        data: {
            labels: [1,2,3,4],
            datasets: [
                {
                label: '1D Mass Error',
                fill: false,
                pointRadius: 0,
                borderColor: 'hotpink',
                borderWidth: 1,

                data: [1,2,3,4]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
					display: true,
					text: 'FM Mass Balance'
				},

            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
	                        gridLines: {
                                drawTicks: false
                            },
					scaleLabel: {
							display: true,
							labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}],
					yAxes: [{
						display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
						scaleLabel: {
							display: true,
							labelString: '%',
                            fontSize: 10,
                            fontColor: 'black',
						}
					}]
				}
        }
    });
'''
    return script

def TUFVolChart():
    script = '''
    var TUFVolChart = new Chart(document.getElementById('TUFVolChart'), {
        type: 'line',
        data: {
            labels: [1,2,3,4],
            datasets: [
                {
                label: 'Vol. In (Stage Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'brown',
                borderWidth: 1,
                data: [1,2,3,4]
                },
                {
                label: 'Vol. Out (Stage Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'hotpink',
                borderWidth: 1,
                data: [2,4,6,8]
                },
                {
                label: 'Vol. In (Flow Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'green',
                borderWidth: 1,
                data: [3,6,9,12]
                },
                {
                label: 'Vol. Out (Flow Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: 'orange',
                borderWidth: 1,
                data: [12,9,6,3]
                },
                {
                label: 'Vol. In (Total)',
                fill: false,
                pointRadius: 0,
                borderColor: 'red',
                borderWidth: 2,
                data: [8,6,4,2]
                },
                {
                label: 'Vol. Out (Total)',
                fill: false,
                pointRadius: 0,
                borderColor: 'blue',
                borderWidth: 2,
                data: [4,3,2,1]
                },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                    display: true,
                    text: 'TUFLOW Volumes'
                },
            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
                        }
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Volume (m3)',
                            fontSize: 10,
                            fontColor: 'black',

                        }
                    }]
                }
        }
    });
    '''
    return script

def TUFMBChart():
    script='''
    var TUFMBChart = new Chart(document.getElementById('TUFMBChart'), {
        type: 'line',
        data: {
            labels: [1,2,3,4],
            datasets: [
                {
                label: 'Cum. Q ME',
                fill: false,
                pointRadius: 0,
                borderColor: 'purple',
                borderWidth: 1,
                data: [1,2,3,4]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                    display: true,
                    text: 'TUFLOW Mass Balance'
                },
            tooltips: {
                mode: 'index',
                intersect: false,
                titleFontSize: 10,
                bodyFontSize: 10,
                displayColors: false
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
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Time',
                            fontSize: 10,
                            fontColor: 'black',
                        }
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            fontSize: 10,
                            fontColor: 'black',
                        },
                        gridLines: {
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true,
                            labelString: '%',
                            fontSize: 10,
                            fontColor: 'black',

                        }
                    }]
                }
        }
    });
    '''
    return script



def layout(simulations):
    layout='''
<div class="grid-container-base">

	<div class="grid-item"></div>

	<div class="grid-item" id="simTitle">Model Log: Simulation Name</div>

	<div>
        <table id = "simulationsList">
            <tr><th colspan="2">Simulations</th></tr>
        	'''+simulations+'''
        </table>
    </div>

    <div class="grid-container-types">
'''
    layout=layout+FMhtml()
    layout=layout+TUFhtml()
    layout=layout+FILhtml()
    layout=layout+'''
    </div>

</div>'''

    return layout

def loadScript():
    script = '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js"></script>
<script>
    window.onload = function show() {
        show1()
    }
</script>

<script>'''

    script = script + FMConChart()
    script = script + FMIOChart()
    script = script + FMItsChart()
    script = script + FMMBChart()
    script = script + TUFVolChart()
    script = script + TUFMBChart()

    script = script + '''
</script>'''

    return script

def updateScript(cursor, sId,sims):
    FMDetTable = ''
    FMModTable = ''
    TUFDetTable = ''
    filesTable = ''

    sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                    FROM simulationExtras, simulations
                    WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 0'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    FMDetTable='''"<tr><th>Parameter</th><th>Value</th></tr>'''
    for item in data:
        FMDetTable = FMDetTable + '''<tr><td>'''+item[0]+'''</td><td>'''+item[1]+'''</td></tr>'''
    FMDetTable = FMDetTable+'''";'''

    sqlCommand = '''SELECT nsParas.parameter
                    FROM nsParas, simulation_nsParas, simulations
                    WHERE simulations.sId = ? and simulation_nsParas.simulationID = simulations.sId and simulation_nsParas.nsParasID = nsParas.nsParasId  and nsParas.software = 0'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    FMModTable='''"<tr><th>Change made</th></tr>'''
    for item in data:
        FMModTable = FMModTable + '''<tr><td>'''+item[0]+'''</td></tr>'''
    FMModTable = FMModTable+'''";'''

    sqlCommand = '''SELECT simulationExtras.parameter, simulationExtras.value
                    FROM simulationExtras, simulations
                    WHERE simulations.sId = ? and simulationExtras.simulationId = simulations.sId and simulationExtras.software = 1'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    TUFDetTable='''"<tr><th>Parameter</th><th>Value</th></tr>'''
    for item in data:
        TUFDetTable = TUFDetTable + '''<tr><td>'''+item[0]+'''</td><td>'''+item[1]+'''</td></tr>'''
    TUFDetTable = TUFDetTable+'''";'''

    sqlCommand = '''SELECT files.fileName, files.fileExt, files.type, files.path, files.readInSettings, files.notes
                    FROM simulation_file, simulations, files
                    WHERE simulations.sId = ? and simulations.sId = simulation_file.simulationID and simulation_file.fileID = files.fId
                    ORDER BY simulations.simName, simulation_file.logOrder'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    filesTable='''"<tr><th>File Name</th><th>File Extension</th><th>File Type</th><th>File Path</th><th>Read in Settings/Notes</th></tr>'''
    for item in data:
        notes=''
        if item[4] and item[5]:
            notes = '<p>'+item[4]+'</p><p>'+item[5]+'</p>'
        elif item[4]:
            notes = item[4]
        elif item[5]:
            notes=item[5]
        filesTable = filesTable + '''<tr><td>'''+item[0]+'''</td><td>'''+item[1]+'''</td><td>'''+item[2]+'''</td><td>'''+item[3].replace('\\','\\\\')+'''</td><td>'''+notes+'''</td></tr>'''
    filesTable = filesTable+'''";'''
    sqlCommand = '''SELECT simulations.simName
                    FROM simulations
                    WHERE simulations.sId = ?'''
    cursor.execute(sqlCommand,[sId])
    simName=cursor.fetchone()[0]

    sqlCommand = '''SELECT FMlf.time, FMlf.flowCon, FMlf.qtol, FMlf.levelCon, FMlf.htol, FMlf.inflow, FMlf.outflow, FMlf.maxitr, FMlf.minitr, FMlf.iterations, FMlf.massError
                    FROM FMlf
                    WHERE FMlf.simulationId = ?
                    ORDER BY FMlf.time'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    fmtdata = list(zip(*data))
    if not fmtdata:
        fmtdata = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

    sqlCommand = '''SELECT TUFmb.time, TUFmb.CumQME, TUFmb.HVolIn, TUFmb.HVolOut, TUFmb.QVolIn, TUFmb.QVolOut, TUFmb.TotVolIn, TUFmb.TotVolOut
                    FROM TUFmb
                    WHERE TUFmb.simulationId = ?
                    ORDER BY TUFmb.time'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    tuftdata = list(zip(*data))
    if not tuftdata:
        tuftdata = [[0],[0],[0],[0],[0],[0],[0],[0]]

    cols=''
    for itemX in sims:
        if itemX[0] == sId:
            cols = cols+'''
                document.getElementById("row'''+str(itemX[0])+'''").style.color = "rgb(255, 255, 255)";
                document.getElementById("row'''+str(itemX[0])+'''").style.backgroundColor = "rgb(0, 0, 0)";
                document.getElementById("row'''+str(itemX[0])+'''").style.fontWeight = "bold";
                '''
        else:
            cols = cols+'''
                document.getElementById("row'''+str(itemX[0])+'''").style.color = "inherit";
                document.getElementById("row'''+str(itemX[0])+'''").style.backgroundColor = "inherit";
                document.getElementById("row'''+str(itemX[0])+'''").style.fontWeight = "inherit";
                '''




    script = '''
    function show'''+str(sId)+'''() {
        '''+cols+'''
        document.getElementById("FMDetTable").innerHTML = '''+FMDetTable+''';
		document.getElementById("FMModTable").innerHTML = '''+FMModTable+''';
		document.getElementById("TUFDetTable").innerHTML = '''+TUFDetTable+''';
		document.getElementById("filesTable").innerHTML = '''+filesTable+''';
		document.getElementById("simTitle").innerHTML =  "Model Log: '''+simName+'''";
        FMConChart.data.datasets[0].data = ['''+', '.join(map(str,fmtdata[1]))+'''];
        FMConChart.data.datasets[1].data = ['''+', '.join(map(str,fmtdata[2]))+'''];
        FMConChart.data.datasets[2].data = ['''+', '.join(map(str,fmtdata[3]))+'''];
        FMConChart.data.datasets[3].data = ['''+', '.join(map(str,fmtdata[4]))+'''];
        FMConChart.data.labels = ['''+', '.join(map(str,fmtdata[0]))+''']
        FMConChart.update()
        FMIOChart.data.datasets[0].data = ['''+', '.join(map(str,fmtdata[5]))+'''];
        FMIOChart.data.datasets[1].data = ['''+', '.join(map(str,fmtdata[6]))+'''];
        FMIOChart.data.labels = ['''+', '.join(map(str,fmtdata[0]))+''']
        FMIOChart.update()
        FMItsChart.data.datasets[0].data = ['''+', '.join(map(str,fmtdata[7]))+'''];
        FMItsChart.data.datasets[1].data = ['''+', '.join(map(str,fmtdata[8]))+'''];
        FMItsChart.data.datasets[2].data = ['''+', '.join(map(str,fmtdata[9]))+'''];
        FMItsChart.data.labels = ['''+', '.join(map(str,fmtdata[0]))+''']
        FMItsChart.update()
        FMMBChart.data.datasets[0].data = ['''+', '.join(map(str,fmtdata[10]))+'''];
        FMMBChart.data.labels = ['''+', '.join(map(str,fmtdata[0]))+''']
        FMMBChart.update()
        TUFVolChart.data.datasets[0].data = ['''+', '.join(map(str,tuftdata[2]))+'''];
        TUFVolChart.data.datasets[1].data = ['''+', '.join(map(str,tuftdata[3]))+'''];
        TUFVolChart.data.datasets[2].data = ['''+', '.join(map(str,tuftdata[4]))+'''];
        TUFVolChart.data.datasets[3].data = ['''+', '.join(map(str,tuftdata[5]))+'''];
        TUFVolChart.data.datasets[4].data = ['''+', '.join(map(str,tuftdata[6]))+'''];
        TUFVolChart.data.datasets[5].data = ['''+', '.join(map(str,tuftdata[7]))+'''];
        TUFVolChart.data.labels = ['''+', '.join(map(str,tuftdata[0]))+''']
        TUFVolChart.update()
        TUFMBChart.data.datasets[0].data = ['''+', '.join(map(str,tuftdata[1]))+'''];
        TUFMBChart.data.labels = ['''+', '.join(map(str,tuftdata[0]))+''']
        TUFMBChart.update()
    }
'''

    return script



def gen(cursor, mId):

    sqlCommand = '''SELECT simulations.sId, simulations.simName
                    FROM simulations, models, model_simulation
                    WHERE models.mId = ? AND model_simulation.modelID = model_simulation.simulationId'''

    cursor.execute(sqlCommand,[mId])
    data=cursor.fetchall()
    #data = data[0:1] # Only do first element


    simulations=''

    script = '''

<script>
'''


    for item in data:
        if item[1].count('_[') == 2:
            simulations = simulations + '''<tr id="row'''+str(item[0])+'''" onclick="show'''+str(item[0])+'''()"><td nowrap>'''+item[1].split('_[')[1][:-1]+'''</td><td>'''+item[1].split('_[')[2][:-1]+'''</td nowrap></tr>'''
        else:
            simulations = simulations + '''<tr id="row'''+str(item[0])+'''" onclick="show'''+str(item[0])+'''()"><td nowrap>'''+item[1]+'''</td></tr>'''

        script = script + updateScript(cursor, item[0],data)

    script = script + '''
</script>
'''

    html = CSS() + layout(simulations) + script + loadScript()

    return html










def generate_log():
    modelName = 'riverTrent'
    dbLoc = r'C:\Users\anthony.cooper\OneDrive - Arup\dev'

    sId = 5
    mId = 1

    #Open Database
    db = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
    cursor = db.cursor()

    #html=generate_header()+generate_content(cursor, mId)
    html = gen(cursor, mId)

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
