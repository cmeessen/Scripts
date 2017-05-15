#!/bin/sh
#
# This script plots a histogram from given x y z values
#
# Christian Meessen, GFZ Potsdam, 2014

if [ $# -lt 2 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: PlotHistogram InputFile nBins [PropertyColumn [HeaderLines]]"
  echo "       arguments in [] are optional"
  echo
  echo "nBins          - Number of bins"
  echo "PropertyColumn - If the InputFile contains multiple columns, this"
  echo "                 defines the column with the value to plot. Columns"
  echo "                 start counting at 0. Default is 2"
  echo "HeaderLines    - Number of header lines in input file"
  echo
  echo "Plots a histogram of the data in the 3rd column."
  echo 
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
elif [ $# -eq 2 ]
then
  FileIn=$1
  nBins=$2
  column=2
  nHeader=""
elif [ $# -eq 3 ]
then
  FileIn=$1
  nBins=$2
  column=$3
  nHeader=""
elif [ $# -eq 4 ]
then
  FileIn=$1
  nBins=$2
  column=$3
  nHeader="-hi$4"
else
  echo "Input arguments: $#"
fi

out_name=$FileIn"_hist.ps"
out_format='png'

zColMin=$(bc <<< "scale=1;($column+1)*2-2")
zColMax=$(bc <<< "scale=1;($column+1)*2-1")

zmin=$(gmt gmtinfo $FileIn -C -o$zColMin $nHeader)
zmax=$(gmt gmtinfo $FileIn -C -o$zColMax $nHeader)

BinWidth=$(bc <<< "scale=10;($zmax-($zmin))/$nBins")

echo "Plot histogram"
echo "> Input: $FileIn"
echo "> ValMin: $zmin"
echo "> ValMax: $zmax"
echo "> Bin count: $nBins"
echo "> Bin width: $BinWidth"

Rmax=$(gmt pshistogram $FileIn -i$column -W$BinWidth -IO -Z1 | gmt gmtinfo -: -C -o1)
STD=$(gmt gmtmath $nHeader -i$column $FileIn STD RINT -Sf =)
MEAN=$(gmt gmtmath $nHeader -i$column $FileIn MEAN -Sf =)
gmt pshistogram $FileIn -i$column -JX10 -W$BinWidth -Bxaf+l"Value range $zmin to $zmax, Stdev: $STD, Mean: $MEAN" --FONT_LABEL=8p -Byaf+l'Frequency' -N0 -Ggray -L1p -Z1 -R$zmin/$zmax/0/$Rmax -BWSne -K > $out_name
STDleft=$(bc <<< "scale=2;$MEAN - $STD")
STDright=$(bc <<< "scale=2;$MEAN + $STD")
echo "$STDleft -100" > stdev.tmp
echo "$STDleft 100" >> stdev.tmp
echo "$STDright 100" >> stdev.tmp
echo "$STDright -100" >> stdev.tmp
gmt psxy stdev.tmp -J -R -W0.5p,black,- -O >> $out_name

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

rm colors.cpt gmt.history gmt.conf $out_name *.eps *.bb stdev.tmp 2> /dev/null

echo "Done."
echo "Output file: "$FileIn"_hist.$out_format"