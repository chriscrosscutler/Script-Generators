#!/bin/python


# The script generator will help you make ANTs scripts to run on the supercomputer.
# Note: You might still get errors while trying to run this script on some participants.
# If that is the case, pay attention to the errors that you are given and you will have to adjust the script accordingly.

# Specifically, this script will generate sbatch scripts to run antsJointLabelFusion.sh on all of the participants in a
# dataset.

from os import listdir

##########################
# CHANGE THESE VARIABLES #
##########################

emailAddress = 'chris.b.cutler@gmail.com'
subjectDir = '/fslhome/ccutle25/compute/Repeatability/Dehydration/Rerun/' # Where are your original subjects found?
antsLocation = '/fslhome/ccutle25/bin/antsbin/bin/' # File path to your ants bin
acpcLocation = '/fslhome/ccutle25/apps/art'
logfilesDir = '/fslhome/ccutle25/logfiles/'
templateLocation = '/fslhome/ccutle25/templates/OASIS/'
c3dLocation = '/fslhome/ccutle25/bin'
scriptDir = '/fslhome/ccutle25/scripts/ants/repeatability/dehydration/rerun/' # Where do you want to save your scripts?
scriptName = 'rerun' # What do you want the name of the scripts to be?
walltime = '50:00:00' # How long will this run? HH:MM:SS

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




"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + str(i) + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1
