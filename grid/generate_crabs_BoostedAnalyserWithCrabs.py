import csv
import os
import das_client
import sys

crab_cfg_path='crab_cfgs_ICHEP_16'
samplelist=sys.argv[1]

csvfile=open(samplelist,'r')
reader = csv.DictReader(csvfile, delimiter=',')#, quotechar='|')
if not os.path.exists(crab_cfg_path):
    os.makedirs(crab_cfg_path)
for row in reader:
    dataset="'"+row['dataset']+"'"
    name=row['name']
    weight=row['weight']
    generator=row['generator']
#    if len(dataset)>3:
#        requestname="'"+(dataset.split('/')[1])+"'"
    if dataset!='' and name!='':
        print 'checking dataset info for',dataset
        das_data=das_client.get_data("https://cmsweb.cern.ch","dataset="+dataset+" instance=phys/prod",0,0,0)
        #print das_data
        #for d in das_data['data']:
	    ##print d
            #for dd in d['dataset']:
	        ##print dd
                #print dd['mcm']['nevents']


        outfilename=crab_cfg_path+'/crab_'+name+'.py'
        if os.path.exists(outfilename):
            for i in range(2,10):
                outfilename=crab_cfg_path+'/crab_'+name+'_v'+str(i)+'.py'
                if not os.path.exists(outfilename):
                    break
        crabout=open(outfilename,'w')
        crab_template=open('crab_cfg_BoostedProducerWithCrabs.py','r')
        for line in crab_template:
            if 'config.Data.inputDataset' in line:
                crabout.write('config.Data.inputDataset = '+dataset+'\n')
            elif 'config.General.requestName' in line:
                crabout.write('config.General.requestName = "'+name+'_76HTT"\n')
            elif 'config.JobType.outputFiles' in line:
                crabout.write('config.JobType.outputFiles = ["BoostedTTH_MiniAOD.root"]\n')#, "'+name+'_JESUP_Tree.root", "'+name+'_JESUP_Cutflow.txt", "'+name+'_JESDOWN_Tree.root", "'+name+'_JESDOWN_Cutflow.txt", "'+name+'_JERUP_Tree.root", "'+name+'_JERUP_Cutflow.txt", "'+name+'_JERDOWN_Tree.root", "'+name+'_JERDOWN_Cutflow.txt"]\n')
            elif 'config.Data.outputDatasetTag' in line:
                crabout.write("config.Data.outputDatasetTag = 'ICHEP-Samples_wHTT-for-80X_"+name+"'\n")
            else:
                crabout.write(line)
        crab_template.close()
        crabout.close()
