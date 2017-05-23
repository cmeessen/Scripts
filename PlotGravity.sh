#!/bin/bash
#
# This script generates quick-and-dirty plots of input files
# Usage: PlotXYZ InputFile [PropertyColumn [HeaderLines]]
#        arguments in [] are optional
#
# PropertyColumn - If the InputFile contains multiple columns, this
#                  defines the column with the value to plot. Columns
#                  start counting at 0. Default is 2
# HeaderLines    - Number of header lines in input file
#
# Note that if header lines in the input file start with different
# characters, i.e. Petrel points with attributes files, you need to define
# the number of header lines.
#
# by Christian Meeßen
# christian.meessen@gfz-potsdam.de
# GFZ Potsdam, 2016

if [ $# -lt 1 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: PlotGravity InputFile [-c][-h][-R][-U]"
  echo "       arguments in [] are optional"
  echo
  echo "c <int>     - If the InputFile contains multiple columns, this"
  echo "              defines the column with the value to plot. Columns"
  echo "              start counting at 0. Default is 2"
  echo "h <int>     - Number of header lines in input file"
  echo "R <ROI>     - Area to plot in GMT -R format xmin/xmax/ymin/ymax"
  echo "U <UTMZONE> - UTM Zone to plot borders and shorelines, e.g. S20 or N10"
  echo
  echo "Plots gravity anomaly data in polar color scale with 0mGal as white and"
  echo "a spacing of 20mGal."
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
fi

# Default parameters
declare -i column
InFile=$1
column=2
nHeader=''
UseROI='False'
ROI=''

# Go through command line options
while (( "$#" ))
do
    if [ "$1" = "-c" ]
    then
        column=$2
        shift 2
    elif [ "$1" = "-h" ]
    then
        nHeader="-hi$2"
        shift 2
    elif [ "$1" = "-R" ]
    then
        UseROI='True'
        ROI="-R$2"
        echo 'Assigned ROI'
        shift 2
    elif [ "$1" = "-U" ]
    then
        utm='True'
        utm_hemi=${2:0:1}
        utm_zone=${2:1}
        if [[ "$utm_hemi" = "S" ]]
        then
            utm_zone="-"$utm_zone
        elif [[ "$utm_hemi" = "N" ]]
        then
            utm_zone="+"$utm_zone
        else
            echo "Unknown utm hemisphere: $utm_hemi"
            exit
        fi
        echo "utm_hemi: $utm_hemi"
        echo "utm_zone: $utm_zone"
        shift 2
    else
        echo "ERROR! Unknown argument $1"
        echo
        exit
    fi
done

# Calculate output column of gmt
declare -i zColMin zColMax
zColMin=($column+1)*2-2
zColMax=($column+1)*2-1

# Get map extent and zvalues
tmp1=(`gmtselect $InFile $ROI $nHeader | gmtinfo -C`)
xmin=${tmp1[0]}
xmax=${tmp1[1]}
ymin=${tmp1[2]}
ymax=${tmp1[3]}
zmin=${tmp1[$zColMin]}
zmax=${tmp2[$zColMax]}

if [[ "$UseROI" = "False" ]]
then
    ROI="-R$xmin/$xmax/$ymin/$ymax"
fi

dX=$(bc <<< "scale=2;$xmax - $xmin")
dY=$(bc <<< "scale=2;$ymax - $ymin")
dZ=20

echo "Defining symmetric color scale"
zminABS=$(bc <<< "sqrt($zmin*$zmin)")
zmaxABS=$(bc <<< "sqrt($zmax*$zmax)")
CScaleMin=$(bc <<< "if ($zminABS < $zmaxABS) -$zmaxABS else -$zminABS")
CScaleMax=$(bc <<< "if ($zminABS < $zmaxABS) $zmaxABS else $zminABS")
# Round to nearest 20
CScaleMin=`bc <<< "scale=0;($CScaleMin/20-1)*20"`
CScaleMax=`bc <<< "scale=0;($CScaleMax/20+1)*20"`
CScale="-T$CScaleMin/$CScaleMax/$dZ"

map_width=10
map_height=$(bc <<< "scale=2;$dY/$dX*$map_width")
scale_dX=$(bc <<< "scale=2;$map_width/2")
out_name=$InFile.ps
out_format='png'

echo "Plot information"
echo "x range [$xmin,$xmax]"
echo "y range [$ymin,$ymax]"
echo "p range [$zmin,$zmax]"
echo "ROI: $ROI"
echo "Color scale $CScale"

gmt set --FONT_ANNOT_PRIMARY=6p\
        --FONT_ANNOT_SECONDARY=6p\
        --FONT_LABEL=6p\
        --FONT_TITLE=8p,Helvetica-Bold\
        --MAP_ANNOT_OFFSET_PRIMARY=0.1\
        --MAP_FRAME_PEN=0.5p\
        --MAP_TICK_LENGTH_PRIMARY=0.1

makecpt -Cpolar.cpt $CScale > colors.cpt
psbasemap $ROI -JX$map_width/$map_height -D$ROI+g'0/0/0/20' -K > $out_name
pscontour $InFile -i0,1,$column $nHeader -I -Ccolors.cpt -J -R -S -W0.1p,black -A- -K -O >> $out_name
psbasemap -R -J -Baf -BwNsE --MAP_GRID_CROSS_SIZE_PRIMARY=0p --MAP_ANNOT_ORTHO=W --MAP_TITLE_OFFSET=8p -O -K >> $out_name
psscale -D$scale_dX/-0.2/$map_width/0.3h -Ccolors.cpt -Baf$dZ+l"Gravity / mGal" -Np --MAP_LABEL_OFFSET=0 -O >> $out_name

case "$out_format" in
bmp )
	ftpe='b';;
eps )
	ftpe='e';;
pdf )
	ftpe='f';;
jpg )
	ftpe='j';;
png )
	ftpe='g';;
* )
	ftpe='g';;
esac

ps2raster -A -P -E400 -T$ftpe $out_name

rm colors.cpt $out_name gmt.history gmt.conf *.eps *.bb 2> /dev/null

echo "Done."
echo "Output file: $InFile.$out_format"
