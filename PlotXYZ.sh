#!/bin/bash
#
# This script generates quick-and-dirty plots of input files
# by Christian Meeßen
# christian.meessen@gfz-potsdam.de
# GFZ Potsdam, 2016

if [ $# -lt 1 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: PlotXYZ InputFile [-col][-c][-head][-I][-R][-t][-U][-v]"
  echo "       arguments in [] are optional"
  echo
  echo "col <int>   - If the InputFile contains multiple columns, this"
  echo "              defines the column with the value to plot. Columns"
  echo "              start counting at 0. Default is 2"
  echo "c <string>  - Name of the GMT color palette."
  echo "head <int>  - Number of header lines in input file"
  echo "I           - Invert colour scale"
  echo "R <ROI>     - Area to plot in GMT -R format xmin/xmax/ymin/ymax"
  echo "U <UTMZONE> - UTM Zone to plot boundaries and rivers, e.g. S20 or N10"
  echo "t <string>  - Title of legend. '_' will be replaced with space"
  echo "v           - Verbose output (debug)"
  echo
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
fi

InFile=$1
column=2
nHeader=''
UseROI='False'
utm='False'
verbose='False'
tlegend='Value'
cpt='-Chaxby'
I=''
shift 1

# Go through command line options
while (( "$#" ))
do
    if [ "$1" = "-col" ]
    then
        column=$2
        shift 2
    elif [ "$1" = "-c" ]
    then
        cpt='-C'$2
        shift 2
    elif [ "$1" = "-head" ]
    then
        nHeader="-hi$2"
        shift 2
    elif [ "$1" = "-I" ]
    then
        I='-I'
        shift 1
    elif [ "$1" = "-R" ]
    then
        UseROI='True'
        ROI="-R$2"
        shift 2
    elif [ "$1" = "-v" ]
    then
        verbose='True'
        shift 1
    elif [ "$1" = "-t" ]
    then
        tlegend=$(echo $2 | sed -e 's/_/ /g')
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

version=`gmt --version`
tick='--'
if [[ $version == "5.4"* ]]
then
  tick=''
fi
gmt set "$tick"FONT_ANNOT_PRIMARY=6p \
        "$tick"FONT_ANNOT_SECONDARY=6p \
        "$tick"FONT_LABEL=6p \
        "$tick"FONT_TITLE=8p,Helvetica-Bold \
        "$tick"MAP_ANNOT_OFFSET_PRIMARY=0.1 \
        "$tick"MAP_FRAME_PEN=0.5p \
        "$tick"MAP_TICK_LENGTH_PRIMARY=0.1


echo 'Plotting '$InFile

if [ "$UseROI" = "False" ]
then
    ROI=$(gmtinfo $InFile -I0.1b $nHeader)
fi
zColMin=$(bc <<< "scale=1;($column+1)*2-2")
zColMax=$(bc <<< "scale=1;($column+1)*2-1")

declare -a fileinfo=(`gmtselect $InFile $ROI $nHeader | gmtinfo -C`)
xmin=${fileinfo[0]}
xmax=${fileinfo[1]}
ymin=${fileinfo[2]}
ymax=${fileinfo[3]}
zmin=${fileinfo[$zColMin]}
zmax=${fileinfo[$zColMax]}

dX=$(bc <<< "scale=2;$xmax - $xmin")
dY=$(bc <<< "scale=2;$ymax - $ymin")
dZ=$(bc <<< "scale=2;($zmax - $zmin)/20")


CScale="-T$zmin/$zmax/$dZ"

map_width=10
map_height=$(bc <<< "scale=2;$dY/$dX*$map_width")
scale_dX=$(bc <<< "scale=2;$map_width/2")
out_name=$InFile.ps
out_format='png'

if [ "$verbose" = 'True' ]
then
    echo "Plot information"
    echo "x range [$xmin,$xmax]"
    echo "y range [$ymin,$ymax]"
    echo "p range [$zmin,$zmax]"
    echo "ROI: $ROI"
    echo "Color scale $CScale"
fi

if [[ "$utm" = "True" ]]
then
    echo "Configuring UTM Projection "$utm_zone" "$utm_hemi
    echo "$xmin $ymin"  > ROI_UTM.dat.tmp
    echo "$xmax $ymax" >> ROI_UTM.dat.tmp
    mapproject ROI_UTM.dat.tmp -JU$utm_zone/12 -R-1/1/-1/1 -F -C -I > ROI_WGS.dat.tmp
    readarray ROI_WGS_arr < ROI_WGS.dat.tmp
    i=0
    for j in ${ROI_WGS_arr[@]}
    do
        ROI_WGS_arr[i]=$(echo $j|tr -d '\n')
        i=$(bc <<< "scale=0;$i+1")
    done
    ROI_WGSr=${ROI_WGS_arr[0]}"/"${ROI_WGS_arr[1]}"/"${ROI_WGS_arr[2]}"/"${ROI_WGS_arr[3]}"r"
    echo ">> ROI_WGSr: $ROI_WGSr"
    pscoastcmd1="-JU$utm_zone/$map_width -R$ROI_WGSr -A0/2/4 -W0.3p,119/138/159 -Di -N1/1p,50/50/50 -N2/0.25p,100/100/100 -W0.25p,119/138/159 -O -P -K"
    pscoastcmd2="-J -R -A0/0/1 -Di -W0.3p,119/138/159 -O -P -K"
    rm -f ROI_UTM.dat.tmp ROI_WGS.dat.tmp
    # echo pscoast1: $pscoastcmd1
    # echo pscoast2: $pscoastcmd2
fi

makecpt $cpt $I $CScale > colors.cpt
pscontour $InFile -i0,1,$column $nHeader -I -Ccolors.cpt -JX$map_width/$map_height $ROI -S -W0.1p,black -A- -K > $out_name
if [[ "$utm" = "True" ]]
then
    pscoast $pscoastcmd1 >> $out_name
    pscoast $pscoastcmd2 >> $out_name
    psbasemap -R$ROI_WGSr -JU$utm_zone/$map_width -Baf -BWS --MAP_ANNOT_ORTHO=W -O -K >> $out_name
    psbasemap $ROI -JX$map_width/$map_height -Baf -BNE --MAP_ANNOT_ORTHO=W -O -K >> $out_name
else
    psbasemap $ROI -JX$map_width/$map_height -Baf -BwsNE --MAP_ANNOT_ORTHO=W -O -K >> $out_name
fi
psscale -D$scale_dX/-0.2/$map_width/0.3h -Ccolors.cpt -Baf$dZ+l"$tlegend" -Np --MAP_LABEL_OFFSET=0 -O >> $out_name

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

rm colors.cpt
rm $out_name
rm gmt.history
rm gmt.conf
rm *.eps *.bb 2> /dev/null

echo "Output file: $InFile.$out_format"
