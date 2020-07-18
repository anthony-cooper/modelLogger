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


    dict = {
        float(0): {
            'inflow': 0,
            'outflow': 0,
            'flowCon': 0,
            'qtol': 0,
            'levelCon': 0,
            'htol': 0,
            'iterations': 0,
            'maxitr': 0,
            'minitr': 0,
            'timestep': 0,
            'massError': 0
        }
    }


    #Read in file
    file = open(lf1File,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:

        data=line.split()
        try: #catch short lines
            if data[0] == '!!Info1':
                if ' '.join(data[1:3]) == 'Mass %error':
                    time = float(data[4])
                    massError = float(data[5])
                    if time in dict:
                        dict[time]['maxitr'] = maxitr
                        dict[time]['minitr'] = minitr
                        dict[time]['qtol'] = qtol
                        dict[time]['htol'] = minitr
                        dict[time]['massError'] = massError
                    else:
                        dict[time] = {
                            'inflow': inflow,
                            'outflow': outflow,
                            'flowCon': flowCon,
                            'qtol': qtol,
                            'levelCon': levelCon,
                            'htol': htol,
                            'iterations': iterations,
                            'maxitr': maxitr,
                            'minitr': minitr,
                            'timestep': timestep,
                            'massError': massError
                        }

                elif data[1] == 'maxitr':
                    maxitr = float(data[3])
                elif data[1] == 'minitr':
                    minitr = float(data[3])
                elif data[1] == 'qtol':
                    qtol = float(data[3])
                elif data[1] == 'htol':
                    htol = float(data[3])

            elif data[0] == '!!PlotI1':
                time = float(data[1])
                iterations = float(data[2])
                timestep = float(data[3])
                if time in dict:
                    dict[time]['iterations'] = iterations
                    dict[time]['timestep'] = timestep
                else:
                    dict[time] = {
                        'inflow': inflow,
                        'outflow': outflow,
                        'flowCon': flowCon,
                        'qtol': qtol,
                        'levelCon': levelCon,
                        'htol': htol,
                        'iterations': iterations,
                        'maxitr': maxitr,
                        'minitr': minitr,
                        'timestep': timestep,
                        'massError': massError
                    }

            elif data[0] == '!!PlotC1':
                time = float(data[1])
                flowCon = float(data[2])
                levelCon = float(round(float(data[3])*float(htol)/float(qtol),4)) # Corrector applied
                if time in dict:
                    dict[time]['flowCon'] = flowCon
                    dict[time]['levelCon'] = levelCon
                else:
                    dict[time] = {
                        'inflow': inflow,
                        'outflow': outflow,
                        'flowCon': flowCon,
                        'qtol': qtol,
                        'levelCon': levelCon,
                        'htol': htol,
                        'iterations': iterations,
                        'maxitr': maxitr,
                        'minitr': minitr,
                        'timestep': timestep,
                        'massError': massError
                    }

            elif data[0] == '!!PlotF1':
                time = float(data[1])
                inflow = float(data[2])
                outflow = float(data[3])
                if time in dict:
                    dict[time]['inflow'] = inflow
                    dict[time]['outflow'] = outflow
                else:
                    dict[time] = {
                        'inflow': inflow,
                        'outflow': outflow,
                        'flowCon': flowCon,
                        'qtol': qtol,
                        'levelCon': levelCon,
                        'htol': htol,
                        'iterations': iterations,
                        'maxitr': maxitr,
                        'minitr': minitr,
                        'timestep': timestep,
                        'massError': massError
                    }




        except:
            raise

    file.close
    # items = dict.items()
    # for item in items:
    #     print(item)

    sorted_dict = sorted(dict.items())

<<<<<<< HEAD
    sorted_dict = sorted(dict.items())

=======
>>>>>>> 58d50beda0eca85802207ece250d46dfe47ba7af
    for item in sorted_dict:
        loggedItems.append((item[0],item[1]['inflow'],item[1]['outflow'],item[1]['flowCon'],item[1]['qtol'],item[1]['levelCon'],item[1]['htol'],item[1]['iterations'],item[1]['maxitr'],item[1]['minitr'],item[1]['timestep'],item[1]['massError']))

    print(loggedItems)
    return loggedItems


<<<<<<< HEAD
#lf1Logger(r'C:\DevArea\TestModel\FM\IEF\Idle_[01-00_CC00]_[__WS-A-02_019].lf1')
=======
lf1Logger(r'C:\DevArea\TestModel\FM\IEF\Idle_[01-00_CC00]_[__WS-A-02_019].lf1')
>>>>>>> 58d50beda0eca85802207ece250d46dfe47ba7af
