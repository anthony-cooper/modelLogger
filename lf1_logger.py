def lf1Logger(lf1File):
    loggedItems =[]
    time=0
    iterations=0
    timestep=0
    flowCon=0
    levelCon=0
    qtol=0
    htol=0
    inflow=0
    outflow=0
    massError=0
    maxitr=0
    minitr=0
    #Read in file
    file = open(lf1File,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:

        data=line.split()
        try: #catch short lines
            if data[0] == '!!Info1':
                if ' '.join(data[1:3]) == 'Mass %error':
                    massError = data[5]
                elif data[1] == 'maxitr':
                    maxitr = data[3]
                elif data[1] == 'minitr':
                    minitr = data[3]
                elif data[1] == 'qtol':
                    qtol = data[3]
                elif data[1] == 'htol':
                    htol = data[3]

            elif data[0] == '!!PlotI1':
                iterations = data[2]
                timestep = data[3]

            elif data[0] == '!!PlotC1':
                flowCon = data[2]
                levelCon = data[3]*htol/qtol # Corrector applied

            elif data[0] == '!!PlotF1':
                time = data[1]
                inflow = data[2]
                outflow = data[3]
                loggedItems.append((time,inflow,outflow,flowCon,qtol,levelCon,htol,iterations,maxitr,minitr,timestep,massError))
        except:
            pass

    file.close

    return loggedItems
