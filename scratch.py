import os

offlinedir = "offline/"
if not os.path.exists(offlinedir):
    os.makedirs(offlinedir)
client = "c2"
op = 'w+'
if os.path.exists(offlinedir+client):
    op = 'a'
f = open(offlinedir+client, op)
f.write('hi there\n')  # python will convert \n to os.linesep
f.write('hi there2\n')
f.close()