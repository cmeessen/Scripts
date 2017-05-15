# /bin/bash
#
# This script triangulates given (irregular) XYZ point data on a sphere and
# outputs a regular Lon Lat Z grid using GMT.
#
# Christian Meessen
# GFZ Potsdam, 2016

if [ $# -lt 7 ]
then
  echo
  echo "Usage: points2grid.sh FILE_IN XMIN XMAX YMIN YMAX SPACING FILE_OUT"
  echo
  echo "Interpolates irregular Lon Lat data on a sphere and outputs"
  echo "a regular Lon Lat Z grid."
  echo
  exit
else
  inFile=$1
  outFile=$7
  xmin=$2
  xmax=$3
  ymin=$4
  ymax=$5
  gridspacing=$6
  
  echo "$inFile"
  echo "*** Triangulate ***"
  gmt sphinterpolate $inFile -R$xmin/$xmax/$ymin/$ymax -i0,1s-1,2 -I$gridspacing -Gtriangle.grd
  
  echo "*** Convert grid to xyz ***"
  gmt grd2xyz triangle.grd > $outFile
  
  echo "*** Cleaning up ***"
  rm gmt.history
  rm triangle.grd
  echo "Done!"
fi
