import os #Used for listing files in folder
import os.path as path #Used for path commands
from TUFLOW_Logger import tuflowLogger
from FloodModeller_Logger import fmLogger
from TLF_Logger import tlfLogger
from ZZD_Logger import zzdLogger



tcfFile = 'FloodModel_~s1~_~e1~.tcf'
#tcfFile = 'Simple.tcf'
tcfPath = r'C:\DevArea\TestModel\Runs'
homePath = r'C:\DevArea\TestModel'
#(Optional)Provide a list of events
events=['','hello']
scenarios=['SEN']
bcEvents = []

iefFile = 'FM_Test.ief'
iefPath = r'C:\DevArea\TestModel\FM'

#loggedItems = tuflowLogger(path.join(tcfPath,tcfFile),homePath,events,scenarios)


for file in os.listdir(iefPath):
    if path.splitext(file)[1].casefold() == '.ief'.casefold():
        loggedItems = fmLogger(path.join(iefPath,file),homePath)

        for loggedItem in loggedItems:
            print(loggedItem)
        print('-------------------------')


tlfPath = r'C:\DevArea\TestModel\FloodModel_BASE_0100.tlf'
loggedItems = tlfLogger(tlfPath)

for loggedItem in loggedItems:
    print(loggedItem)
print('-------------------------')

zzdPath = r'C:\DevArea\TestModel\FM\BROOKSTRAY_[02-00_EP2020-NC]_[TOPO-EXG_CHAN-EXG_001].zzd'
loggedItems = zzdLogger(zzdPath)

for loggedItem in loggedItems:
    print(loggedItem)
print('-------------------------')
