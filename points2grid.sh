# /bin/bash
#
# This script triangulates given (irregular) XYZ point data and outputs a regular
# XYZ grid using GMT.
#
# Christian Meessen
# GFZ Potsdam, 2014

if [ $# -lt 7 ]
then
  echo
  echo "Usage: points2grid FILE_IN XMIN XMAX YMIN YMAX SPACING FILE_OUT"
  echo
  echo "Triangulates given irregular XYZ point data and outputs a regular"
  echo "XYZ grid. For spherical interpolation use points2gridsphere"
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
  gmt triangulate "$inFile" -R$xmin/$xmax/$ymin/$ymax -I$gridspacing -Gtriangle.grd
  
  echo "*** Convert grid to xyz ***"
  gmt grd2xyz triangle.grd > "$outFile"
  
  echo "*** Cleaning up ***"
  rm gmt.history triangle.grd
  echo "Done!"
fi
