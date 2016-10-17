#!/bin/python
from os import listdir

##########################
# CHANGE THESE VARIABLES #
##########################

emailAddress = 'chris.b.cutler@gmail.com'
subjectDir = '/fslhome/ccutle25/compute/Repeatability/ANTsCT/' # Where are your original subjects found?
antsLocation = '/fslhome/ccutle25/bin/antsbin/bin/' # File path to your ants bin
acpcLocation = '/fslhome/ccutle25/apps/art'
logfilesDir = '/fslhome/ccutle25/logfiles/'
templateLocation = '~/templates/repeat_templates/brain/Repeat_template_brain.nii.gz'
c3dLocation = '/fslhome/ccutle25/bin'
scriptDir = '/fslhome/ccutle25/scripts/ants/repeatability/ANTsReg/' # Where do you want to save your scripts?
scriptName = 'repeat_ANTsReg' # What do you want the name of the scripts to be?
walltime = '50:00:00' # How long will this run? HH:MM:SS
out = 'ANTsReg_' #prefix for the output files
Labels = '~/compute/Repeat_template/sub_1/labels/' #where the jlf labels are stored

###################################################################
# ONLY CHANGE THE FOLLOWING SCRIPT IF YOU KNOW WHAT YOU ARE DOING #
###################################################################


dirList=listdir(subjectDir) # Create a list of all of the files and folders in the designated directory.

i=0
for subject in dirList: # Search the designated folder
        t1=(listdir(subjectDir+subject))[0]
        if '.DS_Store' in t1:
                t1=(listdir(subjectDir+subject))[1]
        myScript = (
        """#!/bin/bash
#SBATCH --time=50:00:00 # walltime
#SBATCH --ntasks=2 # number of processor cores (i.e. tasks)
#SBATCH --nodes=1 # number of nodes
#SBATCH --mem-per-cpu=32768M # memory per CPU core
#SBATCH -o """ +logfilesDir+ """output_""" + scriptName + str(i) + """.txt
#SBATCH -e """ +logfilesDir+ """error_""" + scriptName + str(i) + """.txt
#SBATCH -J \"""" + scriptName + str(i) + """\" # job name
#SBATCH --mail-user=""" + emailAddress + """ # email address
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
name=""" +subject+ """
files=""" +subjectDir+ subject+"""
ARTHOME=/fslhome/ccutle25/apps/art/
export ARTHOME
export ANTSPATH=""" + antsLocation + """
PATH=${ANTSPATH}:${PATH}

FIX="""+templateLocation+"""
MOV=${files}/antsCT/ExtractedBrain0N4.nii.gz
INTENSITY=CC[$FIX,${MOV},4,4]

#ANTs Registration
"""+antsLocation+"""ANTS \
3 \
-o ${files}/antsCT/"""+out+""" \
-i 100x100x100x20 \
-t SyN[0.1] \
-r Gauss[3,0.5] \
-m $INTENSITY

"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + str(i) + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1
