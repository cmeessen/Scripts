################################################################################
#                     Copyright (C) 2019 by Christian Meeßen                   #
#                                                                              #
#                        This file is part of GMTScripts.                      #
#                                                                              #
#       GMTScripts is free software: you can redistribute it and/or modify     #
#     it under the terms of the GNU General Public License as published by     #
#           the Free Software Foundation version 3 of the License.             #
#                                                                              #
#      GMTScripts is distributed in the hope that it will be useful, but       #
#          WITHOUT ANY WARRANTY; without even the implied warranty of          #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       #
#                   General Public License for more details.                   #
#                                                                              #
#      You should have received a copy of the GNU General Public License       #
#      along with GMTScripts. If not, see <http://www.gnu.org/licenses/>.      #
################################################################################
import pygmsh as pg
import numpy as np
from collections import OrderedDict

"""
Converts a profile obtained in ParaView to a GMSH *geo file. Requires pygmsh.

IMPORTANT: Currently only works for x=const, i.e. parallely to y-axis. See
TODO.
"""

# TODO: currently only works for profile parallel to the y axis. Add a
#  method to compute the distance along the profile and use this as a local
#  coordinate system to enable usage of arbitrary profiles.


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

    """
    print('Processing', filename)
    vertical_offset = 0
    if BC == 'lower':
        # TODO: Is this necessary? In the example this avoids meshing problems
        #       at the lower boundary. Maybe GMSHs `Coherence` doesnt
        #       properly work?
        vertical_offset = 1
    # Important: columns are loaded in order y,z,x!
    body = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=[1, 2, 0])
    body[:, 1] *= vscale
    body[:, 2] = 0
    coords_top = body[1::2]
    coords_bot = body[::2] - vertical_offset
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
    if BC == 'upper':
        print('> defining upper BC `Top`')
        geom.add_physical_line(lines[:coords_top.shape[0]-1], label='Top')
    elif BC == 'lower':
        print('> defining lower BC `Bottom`')
        geom.add_physical_line(lines[coords_top.shape[0]:-1], label='Bottom')
    # Add line loop
    print('> creating line loops')
    ll = geom.add_line_loop(lines)
    # Make surface
    print('> creating surface')
    ps = geom.add_plane_surface(ll)
    # Make physical surface
    print('> assigning physcial surface name', name)
    geom.add_physical_surface(ps, label=name)


def process(layers, BCs, lcar, geo, vscale=1):
    """
    Start the conversion process.

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
    """
    geom = pg.built_in.Geometry()

    # Obtain the layer polygons
    for layer in layers.keys():
        if layer in BCs.keys():
            BC = BCs[layer]
        else:
            BC = None
        add_surface(layers[layer], layer, geom, lcar, BC, vscale)

    # geom.add_raw_code("Geometry.Tolerance = 1;")
    geom.add_raw_code("Coherence;")

    # Write the file
    f = open(geo, mode='w')
    f.write(geom.get_code())
    f.close()


if __name__ ==  '__main__':
    pass
