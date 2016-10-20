#!/bin/python
# -*- coding: utf-8 -*-
from os import listdir

##########################
# CHANGE THESE VARIABLES #
##########################

emailAddress = 'chris.b.cutler@gmail.com'
subjectDir = '/fslhome/ccutle25/compute/Repeatability/ANTsCT/' # Where are your original subjects found?
antsLocation = '/fslhome/ccutle25/bin/antsbin/bin/' # File path to your ants bin
acpcLocation = '/fslhome/ccutle25/apps/art'
logfilesDir = '/fslhome/ccutle25/logfiles/'
templateLocation = '/fslhome/ccutle25/templates/repeat_templates/brain/'
c3dLocation = '/fslhome/ccutle25/bin'
scriptDir = '/fslhome/ccutle25/scripts/ants/repeatability/WIMT/' # Where do you want to save your scripts?
scriptName = 'repeat_wimt_' # What do you want the name of the scripts to be?
walltime = '50:00:00' # How long will this run? HH:MM:SS
out = 'wimt_' #prefix for the output files
Labels = '~/compute/Repeat_template/sub_1/labels/posteriors/' #where the jlf labels are stored
FIX= '/fslhome/ccutle25/templates/repeat_templates/brain/Repeat_template_brain.nii.gz' # location of the extracted Brain image from your template

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
cd $files
#Warp subject to template
p="""+Labels+"""
for i in $( ls """+Labels+""" ); do

FIXLabel="${i/$p}"
FINALOUT=ants_"${i/$p}"
OUT=${files}/antsCT/ANTsReg_

WarpImageMultiTransform 3 $MOV ${OUT}toTemplate.nii.gz ${OUT}Warp.nii.gz ${OUT}Affine.txt -R """+FIX+"""
WarpImageMultiTransform 3 """+FIX+""" ${OUT}toMov.nii.gz -i ${OUT}Affine.txt ${OUT}InverseWarp.nii.gz -R $MOV
WarpImageMultiTransform 3 $FIXLabel $FINALOUT -i ${OUT}Affine.txt ${OUT}InverseWarp.nii.gz -R $MOV

done
"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + str(i) + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1
