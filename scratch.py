import os
import datetime

offlinedir = "offline/"
try:
    os.makedirs(offlinedir)
except OSError:
    pass
client = "c2"

f = open(offlinedir+client, 'a+')
f.write('hi there' + str(datetime.datetime.now()) + '\n')  # python will convert \n to os.linesep

f.close()

try:
    os.remove(offlinedir+client)
except OSError:
    pass