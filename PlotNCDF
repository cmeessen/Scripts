#!/bin/bash
#
# by Christian Meeßen
# christian.meessen@gfz-potsdam.de
# GFZ Potsdam, 2016

if [ $# -lt 1 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: PlotNCDF InputFile [-i]"
  echo "       arguments in [] are optional"
  echo
  echo "-i    - Activate grid illumination/"
  echo 
  echo "Plots a NetCDF file with or without illumination."
  echo
  exit
elif [ $# -eq 1 ]
then
  InFile=$1
  illum='False'
elif [ $# -eq 2 ]
then
  InFile=$1
  illum='True'
fi

ROI=$(gmt grdinfo $InFile -I-)
xmin=$(gmt grdinfo $InFile -C | awk '{print $2}')
xmax=$(gmt grdinfo $InFile -C | awk '{print $3}')
ymin=$(gmt grdinfo $InFile -C | awk '{print $4}')
ymax=$(gmt grdinfo $InFile -C | awk '{print $5}')
zmin=$(gmt grdinfo $InFile -C | awk '{print $6}')
zmax=$(gmt grdinfo $InFile -C | awk '{print $7}')
dX=$(bc <<< "scale=2;$xmax-($xmin)")
dY=$(bc <<< "scale=2;$ymax-($ymin)")
dZ=$(bc <<< "scale=2;$zmax-($zmin)")
map_width=15
map_height=$(bc <<< "scale=2;$dY/$dX*$map_width")
scale_dX=$(bc <<< "scale=2;$map_width/2")
out_name=$InFile.ps
out_format='png'

#cscale_dZ=$(bc <<< "($dZ/15+0.5)/1")
# echo " color scale dZ: $scale_dZ"
# gmt makecpt -Chaxby -T$zmin/$zmax/$cscale_dZ > colors.cpt
gmt grd2cpt $InFile -Chaxby -E15 > colors.cpt

echo "Plot information"
echo "x range [$xmin,$xmax]"
echo "y range [$ymin,$ymax]"
echo "ROI: $ROI"

gmt set --FONT_ANNOT_PRIMARY=6p \
    --FONT_ANNOT_SECONDARY=6p \
    --FONT_LABEL=6p \
    --FONT_TITLE=8p,Helvetica-Bold \
	--MAP_ANNOT_OFFSET_PRIMARY=0.1 \
    --MAP_FRAME_PEN=0.5p \
    --MAP_TICK_LENGTH_PRIMARY=0.1 \
    --PS_MEDIA=10000x10000

if [ "$illum" == "True" ]
then
    gmt grdgradient $InFile -Nt1 -A60 -Gillumination.nc
    ill='-Iillumination.nc'
else
    ill=''
fi

gmt grdimage $InFile -JX$map_width/$map_height $ROI $ill -Ccolors.cpt -BNsWe -Baf --MAP_ANNOT_ORTHO -K > $out_name
gmt psscale -D$scale_dX/-0.2/$map_width/0.3h -Ccolors.cpt -Baf+l"Value" -Np --MAP_LABEL_OFFSET=0 -O >> $out_name

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

rm gmt.history gmt.conf $out_name colors.cpt
rm *.eps illumination.nc *.bb 2> /dev/null

echo "Done."
echo "Output file: $InFile.$out_format"
