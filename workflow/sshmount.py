#usage python sshmount.py [username] [server] [mountpath] [remotepath]
import os
import sys


def sshmount( uname, sname, mpath, rpath ):
    #---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#

    serverlist = ["naf","lxplus"]

    standardnafworknode = "nafhh-cms02.desy.de"
    standardlxplusworknode = "lxplus6.cern.ch"

    #---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#
    username = uname
    server = sname
    if server not in serverlist:
        print "Only",serverlist,"are allowed"
        exit()


    mountpath = mpath
    if mountpath[0] == "~":
        mountpath = os.path.expanduser("~")+mountpath[1:]
    if not os.path.exists(mountpath):
        print "Mountpath does not exist"
        exit()

    remotepath = rpath
    print "Mounting: "+remotepath+" from "+ server+" @ "+mountpath
    if server == "naf":
        os.system("sshfs "+username+"@"+standardnafworknode+":"+remotepath+" "+mountpath)
    if server == "lxplus":
        os.system("sshfs "+username+"@"+standardlxplusworknode+":"+remotepath+" "+mountpath)




def __main__():
    sshmount(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
