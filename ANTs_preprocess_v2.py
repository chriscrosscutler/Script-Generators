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

subjectDir = 'subject directory' # Where are your original subjects found?
antsLocation = 'ants bin' # File path to your ants bin
acpcLocation = 'acpc location'
logfilesDir = 'log files'
templateLocation = 'template'
c3dLocation = 'c3d'
scriptDir = 'script location' # Where do you want to save your scripts?
scriptName = 'name' # What do you want the name of the scripts to be?
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
#SBATCH -o """ +logfilesDir+ """output_""" + scriptName + subject + """.txt
#SBATCH -e """ +logfilesDir+ """error_""" + scriptName + subject + """.txt
#SBATCH -J \"""" + scriptName + str(i) + """\" # job name

name=""" +subject+ """
files=""" +subjectDir+ subject+"""
ARTHOME=""" +acpcLocation+ """
export ARTHOME
export ANTSPATH=""" + antsLocation + """
PATH=${ANTSPATH}:${PATH}

#ACPCDetect Alignment
echo ACPC align for: $files
""" + acpcLocation + """/acpcdetect \
-M \
-o $files/acpc.nii \
-i $files/t1.nii

# Voxel Resampling to 1x1x1mm Isometric
# Check dataset to see if this is neccessary!!!!
echo Resampling image from $files to 1x1x1mm.
~/apps/c3d/bin/c3d -verbose $files/acpc.nii -resample-mm 1x1x1mm -o $files/resampled.nii.gz

#Skull Stripping
echo Skull Strip
sh /fslhome/ccutle25/bin/antsbin/bin/antsBrainExtraction.sh \
-d 3 \
-a $files/resampled.nii.gz \
-e /fslhome/ccutle25/templates/OASIS/OASIS-30_Atropos_template/T_template0.nii.gz \
-m /fslhome/ccutle25/templates/OASIS/OASIS-30_Atropos_template/T_template0_BrainCerebellumProbabilityMask.nii.gz \
-f /fslhome/ccutle25/templates/OASIS/OASIS-30_Atropos_template/T_template0_BrainCerebellumRegistrationMask.nii.gz \
-o $files/ \
"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + subject + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1
