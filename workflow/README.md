#Scripts for workflow improvements

##scpflow.py
Pythonscript for faster usage of the scp command, when working over ssh. Can be used for upload (-u) and download (-d). Supports SingleFile Mode (-s) and Multifile Modes (-m).
The following system arguments have to be set:
- multiple sourcefiles and one destination
- sourcfiles are listet in .txt file without destinations (filelist and one destination for all files are arguments)
- sourcfiles are listet in .txt file with destinations for each (**only** filelist is an argument)

Works best, when using with a small shell script saved in ~/bin:

    #!/bin/bash
    python path/to/scpflow.py -d $1 server username root/path $2 $3

## cmsswmount and sshmount
Pythonscript that makes mounting CMSSW with sshfs faster. The path that is used to mount the remote folders needs to
exist bevor. For unmounting use:

    fusermount -u /path/to/mount/

Works best, when using with a small shell script saved in ~/bin:
    #!/bin/bash
    python path/to/cmsswmount.py $1 [USERNAME] [SERVER] [SERVERROOT]
