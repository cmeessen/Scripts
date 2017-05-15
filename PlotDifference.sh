#!/bin/bash
#
set -e
setgmt

if [ $# -lt 1 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: PlotDifferences File1 File2 [-col][-head][-R]"
  echo "       arguments in [] are optional"
  echo
  echo "col <int>   - If the InputFile contains multiple columns, this"
  echo "              defines the column with the value to plot. Columns"
  echo "              start counting at 0. Default is 2"
  echo "head <int>  - Number of header lines in input file"
  echo "R <ROI>     - Area to plot in GMT -R format xmin/xmax/ymin/ymax"
  echo
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
fi

File1=$1
File2=$2
column=2
nHeader=''
UseROI='False'
shift 2

# Go through command line options
while (( "$#" ))
do
    if [ "$1" = "-col" ]
    then
        column=$2
        shift 2
    elif [ "$1" = "-head" ]
    then
        nHeader="-hi$2"
        shift 2
    elif [ "$1" = "-R" ]
    then
        UseROI='True'
        ROI="-R$2"
        echo 'Assigned ROI'
        shift 2
    else
        echo "ERROR! Unknown argument $1"
        echo
        exit
    fi
done

if [ "$UseROI" = "False" ]
then
    ROI1=$(gmtinfo $File1 -I0.1b $nHeader)
    ROI2=$(gmtinfo $File2 -I0.1b $nHeader)
    if [ "$ROI1" != "$ROI2" ]
    then
        echo "ERROR! Data extend differs between the files. Specify ROI with -R"
        echo "> $File1: $ROI1"
        echo "> $File2: $ROI2"
        exit
    else
        ROI=$ROI1
    fi
fi

echo "Comparing"
echo "> $File1"
echo "> $File2"

zColMin=$(bc <<< "scale=1;($column+1)*2-2")
zColMax=$(bc <<< "scale=1;($column+1)*2-1")

# Get map extent
tmp1=(`gmtselect $File1 $ROI $nHeader | gmtinfo -C`)
xmin=${tmp1[0]}
xmax=${tmp1[1]}
ymin=${tmp1[2]}
ymax=${tmp1[3]}

# Get minimum and maximum z values
tmp2=(`gmtselect $File2 $ROI $nHeader | gmtinfo -C`)
zmin1=${tmp1[$zColMin]}
zmax1=${tmp1[$zColMax]}
zmin2=${tmp2[$zColMin]}
zmax2=${tmp2[$zColMax]}
zmin=`bc <<< "if($zmin1 < $zmin2) $zmin1 else $zmin2"`
zmax=`bc <<< "if($zmax1 > $zmax2) $zmax1 else $zmax2"`


dX=$(bc <<< "scale=2;$xmax - $xmin")
dY=$(bc <<< "scale=2;$ymax - $ymin")
dZ=$(bc <<< "scale=2;($zmax - $zmin)/20")

CScale="-T$zmin/$zmax/$dZ"

map_width=5
map_height=$(bc <<< "scale=2;$dY/$dX*$map_width")
map_offset=0.5
map_dX=`bc <<< "scale=2;$map_width+$map_offset"`
scale_dX=$(bc <<< "scale=2;$map_width/2")
out_name=$File1'_vs_'$File2'.ps'
out_format='png'

echo "Plot information"
echo "x range [$xmin, $xmax]"
echo "y range [$ymin, $ymax]"
echo "z range [$zmin, $zmax]"
echo "ROI: $ROI"
echo "Color scale $CScale"

scale_dX=$(bc <<< "scale=2;$map_width+$map_offset/2")
scale_dY=$(bc <<< "scale=2;-0.3")
scale_width=$(bc <<< "scale=2;$map_width")

# Preparations
gmt makecpt -Chaxby $CScale > colors.cpt

version=`gmt --version`
tick='--'
if [[ $version == "5.4"* ]]
then
  tick=''
fi
gmt set "$tick"FONT_ANNOT_PRIMARY=6p \
        "$tick"FONT_ANNOT_SECONDARY=6p \
        "$tick"FONT_LABEL=7p \
        "$tick"FONT_TITLE=7p,Helvetica-Bold \
        "$tick"MAP_FRAME_PEN=0.5p \
        "$tick"MAP_LABEL_OFFSET=3p \
        "$tick"MAP_TICK_LENGTH_PRIMARY=1p \
        "$tick"MAP_TICK_LENGTH_SECONDARY=0.5p \
        "$tick"MAP_TITLE_OFFSET=7p \
        "$tick"PS_MEDIA=A4 \
        "$tick"PS_PAGE_ORIENTATION=portrait

###################################
## Plot File1
###################################
title='(a) '$File1
echo $title
pscontour $File1 $nHeader -i0,1,$column $ROI -Ccolors.cpt -JX$map_width/$map_height -W0.1p,black -I -A- -Y10 -K > $out_name
psbasemap -R -J -Baf -BWNse+t"$title" --MAP_ANNOT_ORTHO -O -K >> $out_name
psscale -D$scale_dX/-0.2/$map_width/0.3h -Ccolors.cpt -Baf$dZ+l"Value" -Np -O -K >> $out_name


###################################
## Plot File2
###################################
title='(b) '$File2
echo $title
pscontour $File2 $nHeader -i0,1,$column $ROI -Ccolors.cpt -JX$map_width/$map_height -W0.1p,black -I -A- -X$map_dX -O -K >> $out_name
psbasemap -R -J -Baf -BwNse+t"$title" --MAP_ANNOT_ORTHO -O -K >> $out_name

###################################
## Difference map
###################################

echo 'Calculating difference'
echo '> ROI', $ROI
gmtselect $File1 $ROI $nHeader > File1ROI.tmp
gmtselect $File2 $ROI $nHeader > File2ROI.tmp
gmtmath File1ROI.tmp File2ROI.tmp -C$column SUB = diff.tmp

echo '> Plot properties'
tmp3=(`gmtinfo diff.tmp -C`)
zminDiff=${tmp3[$zColMin]}
zmaxDiff=${tmp3[$zColMax]}
zminDiff2=`bc <<< "scale=5;$zminDiff*($zminDiff)"`
zmaxDiff2=`bc <<< "scale=5;$zmaxDiff*($zmaxDiff)"`
zmin=`bc <<< "if($zminDiff2 < $zmaxDiff2) -1*($zmaxDiff) else $zminDiff"`
zmax=`bc <<< "-1*($zmin)"`
dZ=`bc <<< "scale=2;($zmax-($zmin))/20"`

echo '> Plot'
makecpt -Cpolar -T$zmin/$zmax/$dZ > colors.cpt
pscontour diff.tmp -i0,1,$column $ROI -Ccolors.cpt -I -JX$map_width/$map_height -X$map_dX -O -K >> $out_name
psbasemap -R -J -Baf -BwNsE+t'(c) Difference a-b' --MAP_ANNOT_ORTHO=W -O -K >> $out_name

scale_dX=`bc <<< "scale=2;$map_width/2"`
psscale -D$scale_dX/-0.2/$map_width/0.3h -Ccolors.cpt -Baf$dZ+l"Value" -Np -O >> $out_name

# ###################################
# ## Histogram
# ###################################
# hist_height=$(bc <<< "$map_width")
# map_dX=$(bc <<< "scale=2;-1*$map_width-$map_offset")
# map_dY=$(bc <<< "$hist_height+2")
# echo 'Histogram'
# FileIn=diff.tmp
# BinWidth=20
# Rmax=$(gmt pshistogram $FileIn -i2 -W$BinWidth -IO -Z1 | gmt gmtinfo -: -C -o1)
# STD=$(gmt gmtmath $FileIn -i2 STD RINT -Sf =)
# MEAN=$(gmt gmtmath $FileIn -i2 MEAN RINT -Sf =)
# gmt pshistogram $FileIn -i2 -JX$map_width/$hist_height -R-200/200/0/$Rmax -W$BinWidth -Bxaf+l"Stdev: $STD kg/m@+3@+; Mean: $MEAN kg/m@+3@+" -Byaf+l'Frequency / %' -BwSnE -N0 -Ggray -L1p -Z1e -X$map_dX -Y-$map_dY -O -K >> $out_name
# STDleft=$(bc <<< "scale=2;$MEAN - $STD")
# STDright=$(bc <<< "scale=2;$MEAN + $STD")
# echo "$STDleft -100" > stdev.tmp
# echo "$STDleft 100" >> stdev.tmp
# echo "$STDright 100" >> stdev.tmp
# echo "$STDright -100" >> stdev.tmp
# gmt psxy stdev.tmp -J -R -W0.5p,black,- -O >> $out_name


###################################
## Postprocessing
###################################

echo 'Converting'
ps2raster $out_name -A -Tg -Qt4

rm -rf gmt.history gmt.conf $out_name colors.cpt File1ROI.tmp File2ROI.tmp diff.tmp
rm -rf *.bb *.eps stdev.tmp
