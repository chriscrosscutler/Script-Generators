#!/bin/python

# Note: This script generator will help you make ANTs scripts to run on the supercomputer.
#       It produces a script that resample, N4 bias correct, and skull strip t1 images for each subject in a dataset.
#       It assumes that you have saved the original files as "t1.nii" NOT "t1.nii.gz" in individual directories.

# Note: You might still get errors while trying to run this script on some participants.
#       If that is the case, pay attention to the errors. Many things can go wrong so it is always a good idea to become
#       familiar with the individual steps. Also, pay close attention to your template names. I have the templates named
#       according to the OASIS-30 template, but that will change according to whichever template you choose.

# Note: You will have to adjust the script to match your dataset!

from os import listdir

##########################
# CHANGE THESE VARIABLES #
##########################

emailAddress = 'chris.b.cutler@gmail.com'
subjectDir = '/fslhome/ccutle25/compute/Repeatability/ANTs/' # Where are your original subjects found?
antsLocation = '/fslhome/ccutle25/bin/antsbin/bin' # File path to your ants bin
acpcLocation = '/fslhome/ccutle25/apps/art'
logfilesDir = '/fslhome/ccutle25/logfiles/'
templateLocation = '/fslhome/ccutle25/templates/Repeat/'
c3dLocation = '/fslhome/ccutle25/bin'
scriptDir = '/fslhome/ccutle25/scripts/ants/repeatability/ANTs/pre/' # Where do you want to save your scripts?
scriptName = 'repeat_ANTs_' # What do you want the name of the scripts to be?
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
#SBATCH --time="""+walltime+""" # walltime
#SBATCH --ntasks=1 # number of processor cores (i.e. tasks)
#SBATCH --nodes=1 # number of nodes
#SBATCH --mem-per-cpu=8192M # memory per CPU core
#SBATCH -o """ +logfilesDir+ """output_""" + scriptName + str(i) + """.txt
#SBATCH -e """ +logfilesDir+ """error_""" + scriptName + str(i) + """.txt
#SBATCH -J \"""" + scriptName + str(i) + """\" # job name
#SBATCH --mail-user=""" + emailAddress + """ # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

name=""" +subject+ """
files=""" +subjectDir+ subject+"""
ARTHOME=""" +acpcLocation+ """
export ARTHOME
export ANTSPATH=""" + antsLocation + """
PATH=${ANTSPATH}:${PATH}


############################################################################
#COMMENT OUT ONE OR THE OTHER ACPC ALIGNMENT  METHOD BEFORE RUNNING SCRIPT #
############################################################################

#ACPCDetect Alignment
echo ACPC align for: $files
""" + acpcLocation + """/acpcdetect \
-M \
-o $files/acpc.nii \
-i $files/t1.nii

#Skull Stripping
echo Skull Strip
sh /fslhome/ccutle25/bin/antsbin/bin/antsBrainExtraction.sh \
-d 3 \
-a $files/acpc.nii \
-e /fslhome/ccutle25/templates/Repeat/Repeat_template.nii.gz \
-m /fslhome/ccutle25/templates/Repeat/template_BrainCerebellumProbabilityMask.nii.gz \
-f /fslhome/ccutle25/templates/Repeat/template_BrainCerebellumRegistrationMask.nii.gz \
-o $files/ \
"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + str(i) + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1
