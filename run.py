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
iefPath = r'C:\DevArea\TestModel\FM\IEF'

#loggedItems = tuflowLogger(path.join(tcfPath,tcfFile),homePath,events,scenarios)


for file in os.listdir(iefPath):
    if path.splitext(file)[1].casefold() == '.ief'.casefold():
        loggedItems = fmLogger(path.join(iefPath,file),homePath)

        for loggedItem in loggedItems[0]:
            print(loggedItem)
        print('-------------------------')


tlfPath = r'C:\DevArea\TestModel\Logs\FloodModel_BASE_0100\FloodModel_BASE_0100.tlf'
loggedItems = tlfLogger(tlfPath)

for loggedItem in loggedItems:
    print(loggedItem)
print('-------------------------')

zzdPath = r'C:\DevArea\TestModel\FM\Results\FloodModel_BASE_0100.zzd'
loggedItems = zzdLogger(zzdPath)

for loggedItem in loggedItems:
    print(loggedItem)
print('-------------------------')
