import sqlite3
import os
import random

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
      grid-template-rows: 33% 33% 34%;
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
        min-height: 300px;
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
        <div class="chartDiv-TUFmb" ><canvas id="FMNonConChart"style="width:100%;height:100%;"></canvas></div>

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
                <div class="chartDiv-TUFmb" ><canvas id="TUFdVolChart"style="width:100%;height:100%;"></canvas></div>
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

def FMNonConChart():
    script='''
    var nonConConfig = {
        type: 'scatter',
        data: {
            datasets: [
                {
                label: 'UNLOADED',
                fill: true,
                pointRadius: 3,
                pointBorderColor: 'red',
                pointBackgroundColor: 'red',
                borderWidth: 1,
                data: [{x: 1,y: 2},{x: 3,y: 4},]
                },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                    display: true,
                    text: 'FM Non-Convergence'
                },

            tooltips: {
                mode: 'nearest',
                callbacks: {
      	            title: function(tooltipItems, data) {
                        return data.datasets[tooltipItems[0].datasetIndex].label;
					}
			    },
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
                            labelString: 'Q/H RATIO',
                            fontSize: 10,
                            fontColor: 'black',
                        }
                    }]
                }
        }
    };
    var FMNonConChart = new Chart(document.getElementById('FMNonConChart'), nonConConfig);

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
                borderColor: '#ff00ff',
                borderWidth: 1,
                data: [1,2,3,4]
                },
                {
                label: 'Vol. Out (Stage Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: '#660066',
                borderWidth: 1,
                data: [2,4,6,8]
                },
                {
                label: 'Vol. In (Flow Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: '#ffcc00',
                borderWidth: 1,
                data: [3,6,9,12]
                },
                {
                label: 'Vol. Out (Flow Bdys)',
                fill: false,
                pointRadius: 0,
                borderColor: '#663300',
                borderWidth: 1,
                data: [12,9,6,3]
                },
                {
                label: 'Vol. In (Total)',
                fill: false,
                pointRadius: 0,
                borderColor: '#ff5050',
                borderWidth: 2,
                data: [8,6,4,2]
                },
                {
                label: 'Vol. Out (Total)',
                fill: false,
                pointRadius: 0,
                borderColor: '#993333',
                borderWidth: 2,
                data: [4,3,2,1]
                },
                {
                label: 'Mod. Vol.',
                fill: false,
                pointRadius: 0,
                borderColor: '#00ffff',
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
                    yAxes: [
                    {
                        position: 'left',
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

                    },

                    ]
                }
        }
    });
    '''
    return script

def TUFdVolChart():
    script = '''
    var TUFdVolChart = new Chart(document.getElementById('TUFdVolChart'), {
        type: 'line',
        data: {
            labels: [1,2,3,4],
            datasets: [
                {
                label: 'Change in Mod. Vol. (dVol)',
                fill: false,
                pointRadius: 0,
                borderColor: '#003366',
                borderWidth: 2,
                data: [4,3,2,1]
                },
                {
                label: 'Vol. In - Out',
                fill: false,
                pointRadius: 0,
                borderColor: '#00ff00',
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
                    text: 'TUFLOW Change in Volumes'
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
                    yAxes: [
                    {
                        position: 'left',
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
                            labelString: 'Change in Volume (m3)',
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



def layout(simulations, modelType):
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
    if modelType == 0 or modelType == 2:
        layout=layout+FMhtml()
    if modelType == 1 or modelType == 2:
        layout=layout+TUFhtml()
    layout=layout+FILhtml()
    layout=layout+'''
    </div>

</div>'''

    return layout

def loadScript(modelType):
    script = '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js"></script>
<script>
    window.onload = function show() {
        show1()
    }
</script>

<script>'''
    if modelType == 0 or modelType == 2:
        script = script + FMConChart()
        script = script + FMIOChart()
        script = script + FMItsChart()
        script = script + FMMBChart()
        script = script + FMNonConChart()

    if modelType == 1 or modelType == 2:
        script = script + TUFVolChart()
        script = script + TUFdVolChart()
        script = script + TUFMBChart()

    script = script + '''
</script>'''

    return script

def updateScript(cursor, sId,sims, modelType):
    FMDetTable = ''
    FMModTable = ''
    TUFDetTable = ''
    filesTable = ''

    if modelType == 0 or modelType == 2:

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

    if modelType == 1 or modelType == 2:

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

    if modelType == 0 or modelType == 2:

        sqlCommand = '''SELECT FMlf.time, FMlf.flowCon, FMlf.qtol, FMlf.levelCon, FMlf.htol, FMlf.inflow, FMlf.outflow, FMlf.maxitr, FMlf.minitr, FMlf.iterations, FMlf.massError
                        FROM FMlf
                        WHERE FMlf.simulationId = ?
                        ORDER BY FMlf.time'''
        cursor.execute(sqlCommand,[sId])
        data=cursor.fetchall()
        fmtdata = list(zip(*data))
        if not fmtdata:
            fmtdata = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

    if modelType == 1 or modelType == 2:

        sqlCommand = '''SELECT TUFmb.time, TUFmb.CumQME, TUFmb.HVolIn, TUFmb.HVolOut, TUFmb.QVolIn, TUFmb.QVolOut, TUFmb.TotVolIn, TUFmb.TotVolOut, TUFmb.TotVol, TUFmb.dVol, TUFmb.VolImO
                        FROM TUFmb
                        WHERE TUFmb.simulationId = ?
                        ORDER BY TUFmb.time'''
        cursor.execute(sqlCommand,[sId])
        data=cursor.fetchall()
        tuftdata = list(zip(*data))
        if not tuftdata:
            tuftdata = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

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
        '''+cols
    if modelType == 0 or modelType == 2:
        script = script+'''
        document.getElementById("FMDetTable").innerHTML = '''+FMDetTable+''';
		document.getElementById("FMModTable").innerHTML = '''+FMModTable+''';'''

    if modelType == 1 or modelType == 2:
        script = script+'''
		document.getElementById("TUFDetTable").innerHTML = '''+TUFDetTable+''';'''
    script = script+'''
		document.getElementById("filesTable").innerHTML = '''+filesTable+''';
		document.getElementById("simTitle").innerHTML =  "Model Log: '''+simName+'''";'''
    if modelType == 0 or modelType == 2:
        script = script+'''
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
        nonConConfig.data.datasets.splice(0, 9999)
		FMNonConChart.update()'''
        script = script + fmNonConUpdate(cursor,sId)
    if modelType == 1 or modelType == 2:
        script = script+'''
        TUFVolChart.data.datasets[0].data = ['''+', '.join(map(str,tuftdata[2]))+'''];
        TUFVolChart.data.datasets[1].data = ['''+', '.join(map(str,tuftdata[3]))+'''];
        TUFVolChart.data.datasets[2].data = ['''+', '.join(map(str,tuftdata[4]))+'''];
        TUFVolChart.data.datasets[3].data = ['''+', '.join(map(str,tuftdata[5]))+'''];
        TUFVolChart.data.datasets[4].data = ['''+', '.join(map(str,tuftdata[6]))+'''];
        TUFVolChart.data.datasets[5].data = ['''+', '.join(map(str,tuftdata[7]))+'''];
        TUFVolChart.data.datasets[6].data = ['''+', '.join(map(str,tuftdata[8]))+'''];
        TUFVolChart.data.labels = ['''+', '.join(map(str,tuftdata[0]))+''']
        TUFVolChart.update()
        TUFdVolChart.data.datasets[0].data = ['''+', '.join(map(str,tuftdata[9]))+'''];
        TUFdVolChart.data.datasets[1].data = ['''+', '.join(map(str,tuftdata[10]))+'''];
        TUFdVolChart.data.labels = ['''+', '.join(map(str,tuftdata[0]))+''']
        TUFdVolChart.update()
        TUFMBChart.data.datasets[0].data = ['''+', '.join(map(str,tuftdata[1]))+'''];
        TUFMBChart.data.labels = ['''+', '.join(map(str,tuftdata[0]))+''']
        TUFMBChart.update()'''
    script = script+'''
    }
'''

    return script

def fmNonConUpdate(cursor,sId):
    update = ''
    updates=[]
    sqlCommand = '''SELECT FMNonCons.time, FMNonCons.qRatio, FMNonCons.qRatioNode
                    FROM FMNonCons
                    WHERE FMNonCons.simulationId = ?
                    ORDER BY FMNonCons.qRatioNode'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    series =''
    hex_number ='#000000'
    dataPoints = ''
    count = 0
    maxPoint = 0
    if data:
        for point in data:
            if point[2] != series:
                series = point[2]
                hex_number ='#'+ str(hex(random.randint(0,16777215)))[2:]
                if dataPoints:

                    updates.append((count, hex_number[1:],series,hex_number,dataPoints, maxPoint))
                    dataPoints = ''
                    count=0
                    maxPoint = 0
            dataPoints = dataPoints + '{x:' + str(point[0]) + ', y:' + str(point[1]) + '}, '
            if point[1]> maxPoint:
                maxPoint = point[1]
            count = count + 1

        maxCount = sorted(updates, key=lambda student: student[0] , reverse=True)[0][0]
        maxMaxPoint = sorted(updates, key=lambda student: student[0] , reverse=True)[0][4]
        for item in sorted(updates, key=lambda student: student[0] , reverse=True):
            if item[0]*10>maxCount or item[4]>maxMaxPoint:
                hideLoad = 'false'
            else:
                hideLoad = 'true'

            update = update + '''
            var newDatasetQRatio'''+str(item[1])+''' = {
                label: "Q: '''+item[2]+''' ('''+str(item[0])+''')",
                backgroundColor: "'''+item[3]+'''",
                borderColor: "'''+item[3]+'''",
                borderWidth: 0,
                hidden: '''+hideLoad+''',
                data: ['''+item[4]+''']
            }
            nonConConfig.data.datasets.push(newDatasetQRatio'''+str(item[1])+''');
            '''

    updates=[]
    maxPoint=0
    sqlCommand = '''SELECT FMNonCons.time, FMNonCons.hRatio, FMNonCons.hRatioNode
                    FROM FMNonCons
                    WHERE FMNonCons.simulationId = ?
                    ORDER BY FMNonCons.hRatioNode'''
    cursor.execute(sqlCommand,[sId])
    data=cursor.fetchall()
    series =''
    hex_number ='#000000'
    dataPoints = ''
    count = 0
    if data:
        for point in data:
            if point[2] != series:
                series = point[2]
                hex_number ='#'+ str(hex(random.randint(0,16777215)))[2:]
                if dataPoints:

                    updates.append((count, hex_number[1:],series,hex_number,dataPoints))
                    dataPoints = ''
                    count=0
                    maxPoint=0
            dataPoints = dataPoints + '{x:' + str(point[0]) + ', y:' + str(point[1]) + '}, '
            if point[1]> maxPoint:
                maxPoint = point[1]
            count = count + 1

        maxCount = sorted(updates, key=lambda student: student[0] , reverse=True)[0][0]
        maxMaxPoint = sorted(updates, key=lambda student: student[0] , reverse=True)[0][4]
        for item in sorted(updates, key=lambda student: student[0] , reverse=True):
            if item[0]*10>maxCount or item[4]>maxMaxPoint:
                hideLoad = 'false'
            else:
                hideLoad = 'true'

            update = update + '''
            var newDatasetHRatio'''+str(item[1])+''' = {
                label: "H: '''+item[2]+''' ('''+str(item[0])+''')",
                backgroundColor: "'''+item[3]+'''",
                borderColor: "'''+item[3]+'''",
                borderWidth: 0,
                pointStyle: 'rect',
                hidden: '''+hideLoad+''',
                data: ['''+item[4]+''']
            }
            nonConConfig.data.datasets.push(newDatasetHRatio'''+str(item[1])+''');
            '''





    update = update+ '''


    FMNonConChart.update();'''


    return update


def gen(cursor, mId, modelType):

    sqlCommand = '''SELECT simulations.sId, simulations.simName
                    FROM simulations, models, model_simulation
                    WHERE models.mId = ? AND model_simulation.modelID = model_simulation.simulationId'''

    cursor.execute(sqlCommand,[mId])
    data=cursor.fetchall()
    data = data[0:1] # Only do first element


    simulations=''

    script = '''

<script>
'''


    for item in data:
        if item[1].count('_[') == 2:
            simulations = simulations + '''<tr id="row'''+str(item[0])+'''" onclick="show'''+str(item[0])+'''()"><td nowrap>'''+item[1].split('_[')[1][:-1]+'''</td><td>'''+item[1].split('_[')[2][:-1]+'''</td nowrap></tr>'''
        else:
            simulations = simulations + '''<tr id="row'''+str(item[0])+'''" onclick="show'''+str(item[0])+'''()"><td nowrap>'''+item[1]+'''</td></tr>'''

        script = script + updateScript(cursor, item[0], data, modelType)

        print('generated for: '+ item[1])

    script = script + '''
</script>
'''
    print('************')
    html = CSS() + layout(simulations, modelType) + script + loadScript(modelType)
    print('full html generated')
    return html

def generate_log():
    modelName = 'floodModel'
    dbLoc = r'C:\DevArea\TestDB'

    sId = 5
    mId = 1
    modelType = 2 #0 FM, 1 TUF, 2 Linked

    #Open Database
    db = sqlite3.connect(os.path.join(dbLoc,modelName+'.sqlite3'))
    cursor = db.cursor()

    #html=generate_header()+generate_content(cursor, mId)
    html = gen(cursor, mId, modelType)

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
