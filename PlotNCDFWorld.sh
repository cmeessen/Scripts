#!/bin/bash
#
# This script generates quick-and-dirty plots of input files
# Usage: PlotNCDFWorld InputFile [PropertyColumn [HeaderLines]]
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
  echo "Usage: PlotNCDFWorld InputFile [-i]"
  echo 
  echo "       Optional arguments:"
  echo "           -i    Enable illumination"
  echo
  echo "Plots a NetCDF grid file in Robinson projection."
  echo
  exit
fi

InFile=$1
map_width=10
out_format='png'


echo "Input file: $InFile"

echo "Defining color scale"
gmt grd2cpt $InFile -Chaxby -E21 > colors.cpt

scale_dX=$(bc <<< "scale=2; $map_width/2")
out_name=$InFile.ps

echo "Initiate plot"
gmt gmtset --FONT_ANNOT_PRIMARY=6p --FONT_ANNOT_SECONDARY=6p --FONT_LABEL=6p \
    --FONT_TITLE=8p,Helvetica-Bold --MAP_ANNOT_OFFSET_PRIMARY=0.1 \
    --MAP_FRAME_PEN=0.5p --MAP_TICK_LENGTH_PRIMARY=0.1 --PS_MEDIA=A0 \
    --COLOR_MODEL=rgb
if [ $# -eq 2 ]
then
  if [ "$2" == "-i" ]
  then
    echo "> Illuminating"
    gmt grdgradient $InFile -Nt1 -A60 -Gillumination.nc
    echo "> Ploting"
    gmt grdimage $InFile -JN0/$map_width -Rd -Iillumination.nc -Ccolors.cpt -K > $out_name
  fi
else
  echo "> Ploting"
  gmt grdimage $InFile -JN0/$map_width -Rd -Ccolors.cpt -K > $out_name
fi
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

rm $out_name
rm gmt.history
rm gmt.conf
rm *.eps *.bb colors.cpt illumination.nc 2> /dev/null

echo "Done."
echo "Output file: $InFile.$out_format"
