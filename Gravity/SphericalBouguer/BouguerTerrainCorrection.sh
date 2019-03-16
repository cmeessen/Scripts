#!/bin/bash
###############################################################################
#                     Copyright (C) 2018 by Christian Meeßen                  #
#                                                                             #
#                         This file is part of Scripts                        #
#                                                                             #
#       GMTScripts is free software: you can redistribute it and/or modify    #
#     it under the terms of the GNU General Public License as published by    #
#           the Free Software Foundation version 3 of the License.            #
#                                                                             #
#      GMTScripts is distributed in the hope that it will be useful, but      #
#          WITHOUT ANY WARRANTY; without even the implied warranty of         #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      #
#                   General Public License for more details.                  #
#                                                                             #
#      You should have received a copy of the GNU General Public License      #
#       along with Scripts. If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################
#
# This script calculates a spherical Bouguer correction including terrain
# correction using Tesseroids by L. Uieda.
#
set -e
fFreeAir='./FreeAir_EIGEN-6C4_WGS84.gdf' # The free-air anomaly from ICGEM
fTopo='./ETOPO1.gdf' # Topography with the same bounds and resolution
rhocrust=2670
rhowater=1645 #
dlon=0.0822
dlat=0.0822
dz=1        # Station height above topography

declare -a INFO=(`gmtinfo $fFreeAir -hi35 -i0o-360,1 -C`)
xmin=${INFO[0]}
xmax=${INFO[1]}
ymin=${INFO[2]}
ymax=${INFO[3]}

echo 'Calculating Bouguer terrain correction'
echo '--------------------------------------'
echo 'Topography '$fTopo
echo 'Free-air   '$fFreeAir
echo 'ROI        '$xmin/$xmax/$ymin/$ymax
echo
echo 'Creating station grid'
echo '> Height above topography '$dz' kg/m3'
echo '> Resolution              '$dlon' kg/m3'
xyz2grd $fTopo -hi30 -i0o-360,1,2 -R$xmin/$xmax/$ymin/$ymax -I$dlon -Gtopography.nc
# Replace everything that is < 0 with 0 and add dz
grdmath topography.nc 0 LE 0 topography.nc IFELSE $dz ADD = tessmodel_stations.nc
echo
echo 'Creating density distribution'
echo '> z > 0 : '$rhocrust
echo '> z < 0 : '$rhowater
grdmath topography.nc 0 LE $rhowater $rhocrust IFELSE = tessmodel_densities.nc
echo
echo 'Creating tesseroid model from topography'
echo '> Note: tessmodgen automatically multiplies water densitie by -1 for z < 0'
grd2xyz tessmodel_densities.nc -o2 > tessmodel_densities.tmp
grd2xyz topography.nc > tessmodel_topography.tmp
gmtconvert tessmodel_topography.tmp tessmodel_densities.tmp -A | \
tessmodgen -s$dlon/$dlat -z0 > tessmodel_terrain.dat
echo
echo 'Initiating computation'
tesspar tessmodel_terrain.dat tessmodel_stations.nc -n 90 -nx 10 -o gz_BouguerCorrection.dat
echo
echo 'Subtracting from free-air anomaly'
xyz2grd $fFreeAir -hi35 -i0o-360,1,2 -R$xmin/$xmax/$ymin/$ymax -I$dlon/$dlat -GFreeAir_EIGEN-6C4_WGS84.nc
xyz2grd gz_BouguerCorrection.dat -i0,1,3 -R$xmin/$xmax/$ymin/$ymax -I$dlon/$dlat -Ggz_BouguerCorrection.nc
grdmath FreeAir_EIGEN-6C4_WGS84.nc gz_BouguerCorrection.nc SUB = Bouguer_Full_EIGEN-6C4_WGS84.nc

rm *.tmp
