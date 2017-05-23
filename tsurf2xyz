#!/bin/bash
#
# This script calculates the optimal Delauny triangulated surface from a 
# rectangular Gocad TSurf input file (eg IGMAS+) and creates an equally
# spaced point grid in xyz format.
#
# Christian Meeßen (2014)
#

## Configuration
tsurf_file="Kenya3_Moho.ts"	# Input *.ts
outfile="Kenya3_Moho.xyz"				# Output xyz-gridfile
novalue="9999"					# Value to be set if there is no gridvalue
xmin="-130000"					# Min/Max coordinates of your project
xmax="720000"
ymin="9480000"
ymax="10580000"
gridspacing="10000"				# Gridspacing in m

## The code begins here
clear
echo "*** Extract points from TSurf ***"
awk '($1 == "VRTX") {print $2,$3,$4,$5}' $tsurf_file |sort -n | awk '{print $2,$3,$4}'> table_sorted0.dat
awk '{printf("%1.1f %1.1f %1.3f\n",$1,$2,$3)}' table_sorted0.dat > table_sorted.xyz

## This extracts the triangle-information into a xy-file (optional)
# awk '($1 == "TRGL") {print $2,$3,$4}' $tsurf_file > triangulation.xy

echo "*** Triangulate ***"
gmt triangulate table_sorted.xyz -R$xmin/$xmax/$ymin/$ymax -E$novalue -I$gridspacing -Gtriangle.grd
echo "*** Convert grid to XYZ ***"
gmt grd2xyz triangle.grd > $outfile

echo "*** Deleting unnecessary files ***"
rm table_sorted0.dat
rm table_sorted.xyz
rm triangle.grd
#rm triangulation.xy
rm gmt.history
echo "Done!"