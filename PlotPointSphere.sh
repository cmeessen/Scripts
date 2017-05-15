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

###args=`getopt a:z $*`
###set -- $args
###
###for i
###do
###  echo "--> $i"
###done

if [ $# -lt 3 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: PlotPointSphere InputFile LON0 LAT0 [PropertyColumn [HeaderLines]]"
  echo "       arguments in [] are optional"
  echo
  echo "LON0           - Longitude to look at"
  echo "LAT0           - Latitude to look at"
  echo "PropertyColumn - If the InputFile contains multiple columns, this"
  echo "                 defines the column with the value to plot. Columns"
  echo "                 start counting at 0. Default is 2"
  echo "HeaderLines    - Number of header lines in input file"
  echo
  echo "Plots data points on to a sphere."
  echo 
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
elif [ $# -eq 3 ]
then
  InFile=$1
  LON0=$2
  LAT0=$3
  column=2
  nHeader=""
elif [ $# -eq 4 ]
then
  InFile=$1
  LON0=$2
  LAT0=$3
  column=$4
  nHeader=""
elif [ $# -eq 5 ]
then
  InFile=$1
  LON0=$2
  LAT0=$3
  column=$4
  nHeader="-hi$5"
fi

# I10 - return -R
ROI=$(gmt gmtinfo $InFile -I0.1)
ROID="-Rd"
#CScale=$(gmt gmtinfo $InFile -T1/$column)

zColMin=$(bc <<< "scale=1;($column+1)*2-2")
zColMax=$(bc <<< "scale=1;($column+1)*2-1")

xmin=$(gmt gmtinfo $InFile -C -o0)
xmax=$(gmt gmtinfo $InFile -C -o1)
ymin=$(gmt gmtinfo $InFile -C -o2)
ymax=$(gmt gmtinfo $InFile -C -o3)
zmin=$(gmt gmtinfo $InFile -C -o$zColMin)
zmax=$(gmt gmtinfo $InFile -C -o$zColMax)

dX=$(bc <<< "scale=2;$xmax-($xmin)")
dY=$(bc <<< "scale=2;$ymax-($ymin)")
dZ=$(bc <<< "scale=2;($zmax-($zmin))/20")

CScale="-T$zmin/$zmax/$dZ"

map_width=10
map_height=$(bc <<< "scale=2;$dY/$dX*$map_width")
scale_dX=$(bc <<< "scale=2;$map_width/2")
out_name=$InFile.ps
out_format='png'

echo "Plot information"
echo "Lon range [$xmin,$xmax]"
echo "Lat range [$ymin,$ymax]"
echo "Gz range [$zmin,$zmax]"
echo "ROI: $ROI"
echo "Color scale $CScale"

gmt set --FONT_ANNOT_PRIMARY=6p --FONT_ANNOT_SECONDARY=6p --FONT_LABEL=6p --FONT_TITLE=8p,Helvetica-Bold \
	--MAP_ANNOT_OFFSET_PRIMARY=0.1 --MAP_FRAME_PEN=0.5p --MAP_TICK_LENGTH_PRIMARY=0.1
gmt makecpt -Chaxby.cpt $CScale > colors.cpt
gmt psxy $InFile -i0,1,$column $nHeader -Ss0.1 -W0.01,black -Ccolors.cpt -JG$LON0/$LAT0/10 -Rg -K > $out_name
#  -A0/2/4
# D - resolution
# N - political borders
# W - shorelines
#gmt pscoast -J -R -Di -Na/0.5p,black -O -P -K >> $out_name
gmt pscoast -J -R -A0/0/1 -Di -W0.1p,black -O -P -K >> $out_name
gmt psbasemap -R -J -Baf -BwNsE --MAP_GRID_CROSS_SIZE_PRIMARY=0p --MAP_ANNOT_ORTHO=W --MAP_TITLE_OFFSET=8p -O -K >> $out_name
gmt psscale -D$scale_dX/-0.2/$map_width/0.3h -Ccolors.cpt -Baf$dZ+l"Value" -Np --MAP_LABEL_OFFSET=0 -O >> $out_name

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

rm colors.cpt
rm $out_name
rm gmt.history
rm gmt.conf
rm *.eps *.bb 2> /dev/null

echo "Done."
echo "Output file: $InFile.$out_format"