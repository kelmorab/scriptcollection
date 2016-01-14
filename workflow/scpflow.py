#Usage: python ekplxscp.py [-u or -d] [-m or -s] server user path source(es) [destination]
#              0            1          2         3      4    5    6          7
import sys
import os

"""
if len(sys.argv) != 8:
    print sys.argv, len(sys.argv)
    for i,argv in enumerate(sys.argv):
        print i,":",argv
    print "arguments missing"
    exit()
"""

for i,argv in enumerate(sys.argv):
    print i,":",argv


if sys.argv[1] != "-u" and sys.argv[1] != "-d":
    print "Directon not set. -f or -t as first argument required"
    exit()
if sys.argv[2] != "-m" and sys.argv[2] != "-s":
    print "-m or -s as second argument required"
    exit()
if sys.argv[3] != "naf" and sys.argv[3] != "ekp" and sys.argv[3] != "lxplus":
    print "server: naf, ekp or lxplus"
    exit()
#if inputtype == False and direction == False:
#    print "Please set sys args correctly"
#    exit()


class scp:
    def __init__(self,server,machine,user, path):
        if server == "ekp":
            self.server = "ekplx"+machine+".physik.uni-karlsruhe.de"
        elif server == "naf":
            self.server = "naf-cms.desy.de"
        elif server == "lxplus":
            self.server = "lxplus.cern.ch"
        else:
            print "Error with server"
            exit()
        self.scpstring = user+"@"+self.server+":"+path
        
    def singlefile(self,source, destination, direction):
        print self.scpstring, source, destination
        if direction == "download":
            os.system("scp "+self.scpstring+"/"+source+" "+destination)
        if direction == "upload":
            os.system("scp "+source+" "+self.scpstring+"/"+destination)

    def readsourcefromfile(self, source, direction, destination=None):
        f = open(source, 'r')
        for line in f:
            line = line[:-1]
            inout = line.split(" ")
            if len(line.split(" ")) == 1 and destination != None:
                self.singlefile(line,destination,direction)
            elif len(line.split(" ")) == 2:
                self.singlefile(inout[0],inout[1],direction)
            else:
                print "Error in sourcefile file"
                exit()


if sys.argv[1] == "-u":
    direction = "upload"
elif sys.argv[1] == "-d":
    direction = "download"



copy = scp(sys.argv[3],"91",sys.argv[4],sys.argv[5])
#single file mode
if sys.argv[2] == "-s":
    copy.singlefile(sys.argv[6],sys.argv[7],direction)
#multifile mode: From file with destination
elif sys.argv[2] == "-m" and len(sys.argv) == 7 and sys.argv[6].endswith(".txt"):
    copy.readsourcefromfile(sys.argv[6],direction)
#multifile mode: From file without destination
elif sys.argv[2] == "-m" and sys.argv[6].endswith(".txt"):
    copy.readsourcefromfile(sys.argv[6],direction,sys.argv[7])
#multifile mode: multisourc single destination
elif sys.argv[2] == "-m" and len(sys.argv) > 8:
    filelist = sys.argv[6:len(sys.argv)-1]
    for sourcefile in filelist:
        copy.singlefile(sourcefile,sys.argv[-1],direction)






