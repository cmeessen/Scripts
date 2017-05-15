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
  echo "Usage: PlotGraph InputFile [-col]"
  echo "       arguments in [] are optional"
  echo
  echo "Plots a line graph of the first two colums in InputFile. If different "
  echo "columns shall be plotted define them with col1 and col2"
  echo
  echo "col <int int> - If the InputFile contains multiple columns, this"
  echo "                defines the column with the value to plot. Columns"
  echo "                start counting at 0. Default is 0,1"
  echo "head <int>    - Number of header lines in input file"
  echo "t <string>    - Plot title. '_' will be replaced with space"
  echo "v             - Verbose output (debug)"
  echo 
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
fi

InFile=$1
column=0,1
nHeader=''
verbose='False'
tlegend='Value'
shift 1

# Go through command line options
while (( "$#" ))
do
    if [ "$1" = "-col" ]
    then
        col1=$2
        col2=$3
        shift 3
    elif [ "$1" = "-head" ]
    then
        nHeader="-hi$2"
        shift 2
    elif [ "$1" = "-v" ]
    then
        verbose='True'
        shift 1
    elif [ "$1" = "-t" ]
    then
        tlegend=$(echo $2 | sed -e 's/_/ /g')
        shift 2
    fi
done

echo 'Plotting '$InFile
colxmin=`bc <<< "2*$col1"`
colxmax=`bc <<< "$colxmin+1"`
colymin=`bc <<< "2*$col2"`
colymax=`bc <<< "$colymin+1"`
xmin=$(gmt gmtselect $InFile $nHeader | gmt gmtinfo -C -o$colxmin)
xmax=$(gmt gmtselect $InFile $nHeader | gmt gmtinfo -C -o$colxmax)
ymin=$(gmt gmtselect $InFile $nHeader | gmt gmtinfo -C -o$colymin)
ymax=$(gmt gmtselect $InFile $nHeader | gmt gmtinfo -C -o$colymax)
ROI="$xmin/$xmax/$ymin/$ymax"

dX=$(bc <<< "scale=2;$xmax - $xmin")
dY=$(bc <<< "scale=2;$ymax - $ymin")

map_width=10
map_height=10
scale_dX=$(bc <<< "scale=2;$map_width/2")
out_name=$InFile.ps
out_format='png'

if [ "$verbose" = 'True' ]
then
    echo "Plot information"
    echo "x range [$xmin,$xmax]"
    echo "y range [$ymin,$ymax]"
    echo "ROI: $ROI"
fi

gmt set --FONT_ANNOT_PRIMARY=6p --FONT_ANNOT_SECONDARY=6p --FONT_LABEL=6p --FONT_TITLE=8p,Helvetica-Bold --MAP_ANNOT_OFFSET_PRIMARY=0.1 --MAP_FRAME_PEN=0.5p --MAP_TICK_LENGTH_PRIMARY=0.1

gmt psxy $InFile -i$col1,$col2 -R$ROI -JX$map_width/$map_height -W1p,black -Baf -BWSnE -P > $out_name


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

gmt ps2raster -A -P -E400 -T$ftpe $out_name

rm $out_name
rm gmt.history
rm gmt.conf
rm *.eps *.bb 2> /dev/null

echo "Output file: $InFile.$out_format"