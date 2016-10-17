path=~/compute/Repeat_template/sub_1/labels/posteriors/

for i in $( ls $path ); do
 #get rid of forward slash
FIXLabel="${i/$path}"
echo $FIXLabel
FINALOUT=ants_"${i/$path}"
echo $FINALOUT
OUT=${files}/antsCT/ANTsReg_
echo $OUT
done

for i in $( ls ~/compute/Repeat_template/sub_1/labels/posteriors/ ); do
FIXLabel="${i/~/compute/Repeat_template/sub_1/labels/posteriors/}"
echo fix label:
echo $FIXLabel
FINALOUT=ants_"${i/~/compute/Repeat_template/sub_1/labels/posteriors/}"
echo final out:
echo $FINALOUT
OUT=${files}/antsCT/ANTsReg_
echo out:
echo $OUT
done
