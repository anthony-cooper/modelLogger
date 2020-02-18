
import os.path as path #Used for path commands
from TUFLOW_Logger import tuflowLogger



tcfFile = 'FloodModel_~s1~_~e1~.tcf'
#tcfFile = 'Simple.tcf'
tcfPath = r'C:\DevArea\TestModel\Runs'
homePath = r'C:\DevArea\TestModel'
#(Optional)Provide a list of events
events=['','hello']
scenarios=['SEN']
bcEvents = []



loggedItems = tuflowLogger(path.join(tcfPath,tcfFile),homePath,events,scenarios)
for loggedItem in loggedItems:
     print(loggedItem)
