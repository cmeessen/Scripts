#!/bin/bash
#
# This script generates quick-and-dirty plots of input files
# Usage: PlotXYZ InputFile [PropertyColumn [HeaderLines]]
#        arguments in [] are optional
#
# by Christian Meeßen
# christian.meessen@gfz-potsdam.de
# GFZ Potsdam, 2016

if [ $# -lt 1 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: PlotPoint InputFile [PointSize [PropertyColumn [HeaderLines]]]"
  echo "       arguments in [] are optional"
  echo
  echo "PointSize      - Point size in plot. Default: 0.1"
  echo "PropertyColumn - If the InputFile contains multiple columns, this"
  echo "                 defines the column with the value to plot. Columns"
  echo "                 start counting at 0. Default is 2"
  echo "HeaderLines    - Number of header lines in input file"
  echo
  echo "Plots regular grid data as points."
  echo 
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
elif [ $# -eq 1 ]
then
  InFile=$1
  PointSize=0.1
  column=2
  nHeader=""
elif [ $# -eq 2 ]
then
  InFile=$1
  PointSize=$2
  column=2
  nHeader=""
elif [ $# -eq 3 ]
then
  InFile=$1
  PointSize=$2
  column=$3
  nHeader=""
elif [ $# -eq 4 ]
then
  InFile=$1
  PointSize=$2
  column=$3
  nHeader="-hi$4"
else
  echo "Input arguments: $#"
fi

# I10 - return -R
ROI=$(gmt gmtinfo $InFile -I0.1)
ROI_D=${ROI:2}
#CScale=$(gmt gmtinfo $InFile -T1/$column)

zColMin=$(bc <<< "scale=1;($column+1)*2-2")
zColMax=$(bc <<< "scale=1;($column+1)*2-1")

xmin=$(gmt gmtinfo $InFile -C -o0)
xmax=$(gmt gmtinfo $InFile -C -o1)
ymin=$(gmt gmtinfo $InFile -C -o2)
ymax=$(gmt gmtinfo $InFile -C -o3)
zmin=$(gmt gmtinfo $InFile -C -o$zColMin)
zmax=$(gmt gmtinfo $InFile -C -o$zColMax)

echo "x range [$xmin ; $xmax]"
echo "y range [$ymin ; $ymax]"
echo "z range [$zmin ; $zmax]"

zminBCC=`echo ${zmin} | sed -e 's/[eE]+*/\\*10\\^/'`
zmaxBCC=`echo ${zmax} | sed -e 's/[eE]+*/\\*10\\^/'`

echo "zminBCC: $zminBCC"
echo "zmaxBCC: $zmaxBCC"

dX=$(bc <<< "scale=10;$xmax-($xmin)")
dY=$(bc <<< "scale=10;$ymax-($ymin)")
dZ=$(bc <<< "scale=10;($zmaxBCC-($zminBCC))/20")

echo "dX: $dX"
echo "dY: $dY"
echo "dZ: $dZ"

CScale="-T$zmin/$zmax/$dZ"

map_width=10
map_height=$(bc <<< "scale=2;$dY/$dX*$map_width")
scale_dX=$(bc <<< "scale=2;$map_width/2")
out_name=$InFile.ps
out_format='png'

square_size=$(bc <<< "scale=10;sqrt(2)*($map_width/($dX/10-1))")

echo "Plot information"
echo "ROI: $ROI"
echo "Color scale $CScale"

gmt set --FONT_ANNOT_PRIMARY=6p --FONT_ANNOT_SECONDARY=6p --FONT_LABEL=6p --FONT_TITLE=8p,Helvetica-Bold \
	--MAP_ANNOT_OFFSET_PRIMARY=0.1 --MAP_FRAME_PEN=0.5p --MAP_TICK_LENGTH_PRIMARY=0.1
gmt makecpt -Chaxby.cpt $CScale > colors.cpt
echo "psbasemap"
echo "> ROI: $ROI"
echo "> ROI_D: $ROI_D"
echo "> map_width: $map_width"
echo "> map_height: $map_height"
gmt psbasemap $ROI -JX$map_width/$map_height -D$ROI_D+g'0/0/0' -K > $out_name
#gmt pscontour $InFile -i0,1,$column $nHeader -I -Ccolors.cpt -J -R -S -W0.1p,black -A- -K -O >> $out_name
gmt psxy $InFile -i0,1,$column $nHeader -Ss$PointSize -Ccolors.cpt -R -J -O -K >> $out_name
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