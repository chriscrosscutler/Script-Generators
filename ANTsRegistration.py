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
templateLocation = '/fslhome/ccutle25/templates/repeat_templates/head/'
c3dLocation = '/fslhome/ccutle25/bin'
scriptDir = '/fslhome/ccutle25/scripts/ants/repeatability/ANTsCT/ants/' # Where do you want to save your scripts?
scriptName = 'repeat_ANTsCT_ants_' # What do you want the name of the scripts to be?
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

FIX=${templateLocation}/Repeat_template_brain.nii.gz
MOV=${files}/antsCT/ExtractedBrainN4.nii.gz
INTENSITY=CC[$FIX,${MOV},4,4]

#ANTs Registration
"""+antsLocation+"""ANTS \
3 \
-o """+out+""" \
-i 100x100x100x20 \
-t SyN[0.1] \
-r Gauss[3,0.5] \
-m $INTENSITY

#Warp subject to template
for i in{ls """+Labels+"""}; do
path=/path/to/labels/

FIXLabel=“${i/$path}”
FINALOUT=ants_”${i/$path}"

WarpImageMultiTransform $DIM $MOV ${OUT}toTemplate.nii.gz ${OUT}Warp.nii.gz ${OUT}Affine.txt -R $FIX
WarpImageMultiTransform $DIM $FIX ${OUT}toMov.nii.gz -i ${OUT}Affine.txt ${OUT}InverseWarp.nii.gz -R $MOV
WarpImageMultiTransform $DIM $FIXLabel $FINALOUT -i ${OUT}Affine.txt ${OUT}InverseWarp.nii.gz -R $MOV

#thresh/binarize each ROI
#c3d <input.nii.gz> -thresh 0.3 1 1 0 <output.nii.gz>

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
