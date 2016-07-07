#usage python cmsswmount.py [version] [username] [server] [serveroot]
import sys

from sshmount import sshmount


def mountcmssw(version, username, server, serverroot):
    #---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#

    versionlist = ["8_0_10","7_6_3"]

    #---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------#

    if version not in versionlist:
        print version,"is not supported"
        exit()
    print version
    if version == "8_0_10":
        cmsswpostfix = "CMSSW_8_0_10/src/"
    elif version == "7_6_3":
        cmsswpostfix = "CMSSW_7_6_3/src/"
    else:
        print "exiting"
        exit()

    sshmount(username, server, "~/sshmount/CMSSW", serverroot+cmsswpostfix)


def main():
    mountcmssw(str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))


if __name__ == "__main__":
    main()
