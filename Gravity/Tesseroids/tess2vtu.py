# coding=utf-8
###############################################################################
#                     Copyright (C) 2019 by Christian Meeßen                  #
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
"""
tess2vtu

This script converts a tesseroid model created with the tool tesseroids
(http://tesseroids.leouieda.com) into a vtu file that, e.g. can be opened with
ParaView.

Christian Meeßen, 2018
"""

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print 'Not enough arguments!'
        print 'Usage: tess2vtu FilIn'
        sys.exit()

    import numpy as np
    import os

    fmodel = sys.argv[1]
    fvtu = os.path.splitext(fmodel)[0]+'.vtu'

    raw_model = np.loadtxt(fmodel)

    """
    A vtu file consists of the following xml blocks

    <Points>
      <DataArray type="Float32" NumberOfComponents="3" format="ascii">
        X1 Y1 Z1
        ...
      </DataArray>
    </Points>
    <Cells>
      <DataArray type="Int32" Name="connectivity" format="ascii">
        P1 P2 P3 P4 P5 P6 P7 P8 # Point indices that constitute one cell
        ...
      </DataArray>
      <DataArray type="Int32" Name="offsets" format="ascii">
        NPointsCell1 NPointsCell1+NPointsCell2 .
      </DataArray>
    """

    points = []
    connectivity = []
    prop_dens = []
    P8 = -1
    for p in raw_model:
        [W, E, S, N, top, bot, dens] = p
        points.append([W, N, top])
        points.append([E, N, top])
        points.append([E, S, top])
        points.append([W, S, top])
        points.append([W, N, bot])
        points.append([E, N, bot])
        points.append([E, S, bot])
        points.append([W, S, bot])
        P1 = P8 + 1
        P2 = P1 + 1
        P3 = P2 + 1
        P4 = P3 + 1
        P5 = P4 + 1
        P6 = P5 + 1
        P7 = P6 + 1
        P8 = P7 + 1
        prop_dens.append(dens)
        connectivity.append([P1, P2, P3, P4, P5, P6, P7, P8])

    npoints = len(points)
    ncells = len(connectivity)
    offsets = range(8, ncells*8+8, 8)

    f = open(fvtu, 'w')

    h = '<?xml version="1.0"?>\n' \
        '<VTKFile type="UnstructuredGrid" version="0.1" ' \
        'byte_order="LittleEndian">\n' \
        '  <UnstructuredGrid>\n' \
        '    <Piece NumberOfPoints="{0}" NumberOfCells="{1}">\n' \
        '      <Points>\n' \
        '        <DataArray type="Float32" NumberOfComponents="3" ' \
        'format="ascii">\n'.format(str(npoints), str(ncells))
    f.write(h)
    for p in points:
        f.write('          {0} {1} {2}\n'.format(str(p[0]),
                                                 str(p[1]),
                                                 str(p[2])))
    h = '        </DataArray>\n' \
        '      </Points>\n' \
        '      <Cells>\n' \
        '        <DataArray type="Int32" Name="connectivity" format="ascii">\n'
    f.write(h)
    for p in connectivity:
        f.write('          {0} {1} {2} {3} {4} {5} {6} {7}\n'.format(str(p[0]),
                                                                     str(p[1]),
                                                                     str(p[2]),
                                                                     str(p[3]),
                                                                     str(p[4]),
                                                                     str(p[5]),
                                                                     str(p[6]),
                                                                     str(p[7])))
    h = '        </DataArray>\n' \
        '        <DataArray type="Int32" Name="offsets" format="ascii">\n'
    f.write(h)
    i = 0
    for p in offsets:
        if i == 0:
            f.write('          ')
        else:
            f.write(' ')
        f.write(str(p))
        if i == 9:
            f.write('\n')
            i = 0
        else:
            i += 1
    h = '        </DataArray>\n' \
        '        <DataArray type="Int32" Name="types" format="ascii">\n'
    f.write(h)
    i = 0
    for p in offsets:
        if i == 0:
            f.write('          ')
        else:
            f.write(' ')
        f.write('12')
        if i == 9:
            f.write('\n')
            i = 0
        else:
            i += 1
    h = '        </DataArray>\n' \
        '      </Cells>\n' \
        '      <CellData Scalars="PROPERTIES">\n' \
        '        <DataArray type="Float64" Name="Density" format="ascii">\n'
    f.write(h)
    for p in prop_dens:
        f.write('          '+str(p)+'\n')
    h = '        </DataArray>\n' \
        '      </CellData>\n' \
        '    </Piece>\n' \
        '  </UnstructuredGrid>\n' \
        '</VTKFile>\n'
    f.write(h)
    f.close()
