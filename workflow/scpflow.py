#+-------------------------------------------------------------------------------------------------------------------+
# Script for improving workflow, when using scp on multiple files
# 2016, K. Schweiger
#
# Usage: python ekplxscp.py (-u or -d) (-m or -s) server user path source[es] [destination]
# (..): mandatory, [..]: voluntary, -u: Upload, -d: Download
# -s: Single file mode -> When uploading, the destination is voluntary and the file is copyed wo the location 
#                         specified in the path argument
#                      -> When downloading, the destination is manatory (current folder with .)
# -m: Multi file mode  -> Destination, when up- or downloading: see -s
#                      -> Possible usage: multiple sourcefiles as argument (onload upload)
#                                         sourcefile is list of files -> no destination as argument, when 
#                                                                        setting destination in sourcefile
#                                                                     -> destination mandatory, when source 
#                                                                        file only contains files without destination
#                      -> List of files as sourcefile: /path/to/file [/destination/on/server/rel/to/path/argv]
#+-------------------------------------------------------------------------------------------------------------------+

import sys
import os

screenoutput = False

if screenoutput:
    for i,argv in enumerate(sys.argv):
        print i,":",argv


if sys.argv[1] != "-u" and sys.argv[1] != "-d":
    print "Directon not set. -f or -t as first argument required"
    exit()
if sys.argv[2] != "-m" and sys.argv[2] != "-s":
    print "-m or -s as second argument required"
    exit()
if sys.argv[3] != "naf" and (sys.argv[3])[0:5] != "ekplx" and sys.argv[3] != "lxplus":
    print "server: naf, ekp or lxplus"
    exit()


class scp:
    def __init__(self,server,user, path):
        if server[0:5] == "ekplx":
            self.server = server+".physik.uni-karlsruhe.de"
        elif server == "naf":
            self.server = "naf-cms.desy.de"
        elif server == "lxplus":
            self.server = "lxplus.cern.ch"
        else:
            print "Error with server"
            exit()
        self.scpstring = user+"@"+self.server+":"+path
        
    def singlefile(self,source, destination, direction):
        if screenoutput:
            print direction+": "+self.scpstring+"/"+source+" to "+destination
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



copy = scp(sys.argv[3],sys.argv[4],sys.argv[5])
#single file mode
if sys.argv[2] == "-s":
    if len(sys.argv) == 7:
        copy.singlefile(sys.argv[6],"",direction)
    else:
        copy.singlefile(sys.argv[6],sys.argv[7],direction)
#multifile mode: From file with destination
elif sys.argv[2] == "-m" and len(sys.argv) == 7 and sys.argv[6].endswith(".txt") and direction == "upload":
    copy.readsourcefromfile(sys.argv[6],direction)
#multifile mode: From file without destination
elif sys.argv[2] == "-m" and sys.argv[6].endswith(".txt"):
    copy.readsourcefromfile(sys.argv[6],direction,sys.argv[7])
#multifile mode: multisourc single destination
elif sys.argv[2] == "-m" and len(sys.argv) > 8:
    filelist = sys.argv[6:len(sys.argv)-1]
    for sourcefile in filelist:
        copy.singlefile(sourcefile,sys.argv[-1],direction)






