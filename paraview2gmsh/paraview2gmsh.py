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
import pygmsh as pg
import numpy as np
from collections import OrderedDict

"""
Converts a profile obtained from a GMS model in ParaView to a GMSH *geo file.
Requires pygmsh.
"""

def compute_distance(array):
    """ Compute distance and sort array"""
    x = array[:,0]
    y = array[:,1]
    # Make a structured array for sorting
    dtypes = [('d', 'f8'), ('z', 'f8'), ('y', 'f8')]
    newarr = np.zeros(array.shape[0], dtype=dtypes)
    newarr['d'] = np.sqrt((x[0] - x)**2 + (y[0] - y)**2)
    newarr['z'] = array[:,2]
    newarr.sort(order=['d', 'z'])
    # Convert back to ndarray
    oldshape = newarr.shape
    return newarr.view(np.float64).reshape(oldshape+(-1,))

def add_surface(filename, name, geom, lcar, BC=None, vscale=1):
    """
    Adds a surface to an existing geometry file.

    Parameters
    ----------
    filename : str
    name : str
        Name of the layer
    geom : pygmsh.built_in.geometry.Geometry()
        The Geometry object where the points should be added to.
    lcar : float
        The characteristic length of the points.
    BC : str
        Defines location of a boundary in the body. Can be `upper` or `lower`.
    vscale : float
        Scale the data z-axis by this value.

    Returns
    -------
    line_BC_left, line_BC_right : lists
        Lists of lines that constitute the left and right boundary
    """
    print('Processing', filename)
    # Important: columns are loaded in order y,z,x!
    # body = np.genfromtxt(filename, delimiter=',', skip_header=1,
                        #  usecols=[1,2,0], names=['y','z','x'])
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    body = compute_distance(data)
    # Convert back to a ndarray
    body[:, 1] *= vscale
    coords_top = body[1::2]
    coords_bot = body[::2]
    coords = np.concatenate((coords_top, coords_bot[::-1]))
    # Add points
    points = []
    lines = []

    print('> adding points')
    for row in coords:
        points.append(geom.add_point(row, lcar))

    print('> creating lines')
    for i in range(len(points)-1):
        lines.append(geom.add_line(points[i], points[i+1]))
    lines.append(geom.add_line(points[-1], points[0]))

    line_BC_left = None
    line_BC_right = None
    p0, p1 = lines[-1].points
    if np.linalg.norm(p0.x - p1.x) > 0:
        line_BC_left = lines[-1]
    line_id = int(len(lines)/2 - 1)
    p0, p1 = lines[line_id].points
    if np.linalg.norm(p0.x - p1.x) > 0:
        line_BC_right = lines[line_id]

    if BC == 'upper':
        print('> defining upper BC `Top`')
        geom.add_physical_line(lines[:coords_top.shape[0]-1], label='Top')
    elif BC == 'lower':
        print('> defining lower BC `Bottom`')
        geom.add_physical_line(lines[coords_top.shape[0]:-1], label='Bottom')

    print('> creating line loops')
    ll = geom.add_line_loop(lines)

    print('> creating surface')
    ps = geom.add_plane_surface(ll)

    print('> assigning physcial surface name', name)
    geom.add_physical_surface(ps, label=name)

    return line_BC_left, line_BC_right


def process(layers, BCs, lcar, geo, vscale=1, tolerance=1e-7):
    """
    Starts the conversion process and writes the geo-file. The boundary names
    are `Top`, `Bottom`, `Left` and `Right`.

    Parameters
    ----------
    layers : collections.OrderedDict
        Ordered dictionary with {layername:file}. Should be ordered from top to
        bottom
    BCs : dict
        Defines the layers where boundary conditions are {layername:BC} where
        BC either `upper` or `lower`
    lcar : float
        The characteristic length defining the resolution
    geo : str
        Output file name
    vscale : float
        Scale the data z-axis by this value.
    tolerance : float
        The tolerance for gmsh to remove invalid geometries. This might have to
        be adjusted depending on the mesh.
    """
    geom = pg.built_in.Geometry()
    geom.add_raw_code('Geometry.AutoCoherence = 2;')
    geom.add_raw_code('Geometry.Tolerance = '+str(tolerance)+';')

    line_BC_left = []
    line_BC_right = []
    # Obtain the layer polygons
    for layer in layers.keys():
        if layer in BCs.keys():
            BC = BCs[layer]
        else:
            BC = None
        left, right = add_surface(layers[layer], layer, geom, lcar, BC, vscale)
        if left is not None:
            line_BC_left.append(left)
        if right is not None:
            line_BC_right.append(right)
    geom.add_physical_line(line_BC_left, label='Left')
    geom.add_physical_line(line_BC_right, label='Right')
    geom.add_raw_code('Coherence;')

    # Write the file
    f = open(geo, mode='w')
    f.write(geom.get_code())
    f.close()


if __name__ ==  '__main__':
    pass
