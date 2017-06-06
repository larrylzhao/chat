import os
import datetime
import shutil

offlinedir = "offline/"
try:
    os.makedirs(offlinedir)
except OSError:
    pass
client = "c2"

f = open(offlinedir+client, 'a+')
f.write('hi there' + str(datetime.datetime.now()) + '\n')

f.close()

try:
    shutil.rmtree(offlinedir)
except OSError:
    pass