# import os
# import datetime
import shutil
#
offlinedir = "offline/"
# try:
#     os.makedirs(offlinedir)
# except OSError:
#     pass
client = "c2"
#
# f = open(offlinedir+client, 'a+')
# f.write('hi there' + str(datetime.datetime.now()) + '\n')
#
# f.close()
# #
# # try:
shutil.rmtree(offlinedir+client)
# # except OSError:
# #     pass
#
# try:
#     with open('offline/c2') as f:
#         content = f.readlines()
#     content = [x.strip() for x in content]
#     print "content: " + str(content)
#     for message in content:
#         print "m: " + message
#     # f = open(offlinedir+client, 'r')
#     # list = f.read()
#     # for item in list:
#     #     item.strip()
#     #     print item
# except:
#     print "failed"
