# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 13:12:21 2016

Calculate the isostatic density distribution of a layer assuming a density
distribution in the mantle. The calculation utilises thickness maps and
configuration files from GMS models.

Parameters:

    * flay : str
        File name for *_lay.dat

    * fdensmantle : str
        File name for mantle density distribution

    * mantle : str
        Layer name for mantle

    * crust : str
        The layer name in the model that will be isostatically adjusted

    * targetload : float
        Target load at the bottom of the model in Pa

    * fout : str
        Output file name for layer density

@author: chmee
"""

import numpy as np
import sys
import time

def grd2tab(grd, xmin, xmax, ymin, ymax):
    """
    Take a 2D array and convert it to a table containing x,y,z.

    Parameters:

    * grd : numpy array
        2D Array of structure [x, y]

    * [xmin, xmax, ymin, ymax] : float
        Extents of the grid points in grd

    Returns:

    * arr : numpy array
        Array in table-style of structure [rows, 3].
    """
    nx, ny = grd.shape
    dx = (xmax - xmin)/(nx - 1)
    dy = (ymax - ymin)/(ny - 1)
    arr = np.empty([nx*ny, 3])
    row = 0
    for x in range(nx):
        for y in range(ny):
            arr[row, 0] = xmin + x*dx
            arr[row, 1] = ymin + y*dy
            arr[row, 2] = grd[x, y]
            row += 1
    return arr

def ShowHelp():
    print
    print "Calculates the isostatic density distribution of a layer assuming a"
    print "density distribution in the mantle. The calculation utilises"
    print "thickness maps and configuration files from GMS models. For"
    print "required files see section below. The mantle density distribution"
    print "must be a 2D grid file, not a voxel! Use the script VoxelAverage to"
    print "calculate 2D average grids from 3D voxels."
    print
    print "Usage: VoxelIsostasy GMSName Load [optional parameters]"
    print
    print "   GMSName  GMS Project name"
    print "   Load     Load at model base in GPa"
    print
    print "Optional parameters:"
    print "   -vox     Filename of input density distribution. Default file"
    print "            name: DensityMantle.dat. The input file must be a "
    print "            X Y Z file."
    print "   -lm      Mantle layer name. Default: LithMantle"
    print "   -lc      Crustal layer name. Default: Crust"
    print "   -out     Output file name."
    print
    print "Required input files:"
    print "   - lay.dat"
    print "   - strat.dat"
    print "   - surface (same name as in strat.dat)"
    print "   - thickness maps (name: t_layer.dat)"
    print
    sys.exit()

if __name__ == "__main__":
    # Default values
    fdensmantle = 'DensityMantle.dat'
    crust = 'Crust'
    mantle = 'LithMantle'
    usevox = False
    fout = None
    tstart = time.ctime()

    # Read command line arguments
    n_args = len(sys.argv)
    if n_args > 1 and sys.argv[1] == "-h":
        ShowHelp()
    if n_args < 3:
        print
        print "Error: not enough arguments!"
        # print "Usage: VoxelIsostasy PROJECT LOAD [-vox|-lm|-lc|-out|-h]"
        ShowHelp()
        sys.exit()
    project = sys.argv[1]
    targetloadGPa = float(sys.argv[2])
    targetload = targetloadGPa*1E9
    i = 3
    while i < n_args:
        if sys.argv[i] == '-vox':
            fdensmantle = sys.argv[i + 1]
            usevox = True
            i+=1
        elif sys.argv[i] == '-lc':
            crust = sys.argv[i + 1]
            i+=1
        elif sys.argv[i] == '-lm':
            mantle = sys.argv[i + 1]
            i+=1
        elif sys.argv[i] == '-out':
            fout = sys.argv[i + 1]
            i+=1
        i += 1

    if fout is None:
        fout = project + '_RhoCrust_' + str(targetloadGPa) + 'GPa.dat'

    fstrat = project + '_strat.dat'
    flay = project + '_lay.dat'
    strat = np.genfromtxt(fstrat, dtype=None, comments='/', usecols=(2))
    fsurf = strat[-1]
    crustidx = None

    g = 9.81

    print 'Importing data'
    surface = np.loadtxt(fsurf, usecols=(0, 1, 2))
    if usevox:
        densmantle = np.loadtxt(fdensmantle, usecols=(0, 1, 2))
        print 'Testing data integrity'
        if surface.shape == densmantle.shape:
            print '> Number of points ok'
        else:
            print
            print "ERROR: Mismatch in points between GMS model and mantle density"
            print "Surface shape       :", surface.shape
            print "Mantle density shape:", densmantle.shape
            print
            sys.exit()
        if np.equal(surface[:, 0], densmantle[:, 0]).all():
            print '> X-coords ok'
        else:
            print
            print "ERROR: X-coords of GMS model and mantle density are unequal"
            print
            sys.exit()
        if np.equal(surface[:, 1], densmantle[:, 1]).all():
            print '> Y-coords ok'
        else:
            print
            print "ERROR: Y-coords of GMS Model and mantle density are unequal"
            print
            sys.exit()

    print 'Loading', flay
    laydat = np.genfromtxt(flay, dtype=None)
    layers=[]       # Array containing layer names
    densities=[]    # Contains densities for each layer
    thickness=[]    # Contains thickness information
    i = 0
    for elem in laydat:
        print '> Processing', elem[0]
        layers.append(elem[0])
        densities.append(elem[1])
        fthick = "t_" + elem[0] + ".dat"
        thickness.append(np.loadtxt(fthick, usecols=(0, 1, 2)))
        if elem[0] == crust:
            crustidx = i
        i+=1

    if crustidx is None:
        print 'Error: layer', crust, 'not found in ', flay
        sys.exit()

    print 'Transferring data tables to arrays'
    xmin, ymin, tmp = surface.min(0)
    xmax, ymax, tmp= surface.max(0)
    xvals = np.unique(surface[:, 0])
    yvals = np.unique(surface[:, 1])
    dx = xvals[1] - xvals[0]
    dy = yvals[1] - yvals[0]
    nx = len(xvals)
    ny = len(yvals)
    nlay = len(layers)
    # 4th dimension in model array contains thickness [0] and density [1] at
    # each point
    model = np.empty([nx, ny, nlay, 2])
    for i in range(nlay):
        # Go through each coordinate and assign thickness and density
        print '> Processing layer: ' + layers[i]
        row = 0
        for point in thickness[i]:
            xarr = int((point[0] - xmin)/dx)
            yarr = int((point[1] - ymin)/dy)
            # Assign thickness
            model[xarr, yarr, i, 0] = point[2]
            if layers[i] != mantle:
                # Assign layer density
                model[xarr, yarr, i, 1] = densities[i]
            else:
                # Assign mantle density
                if usevox:
                    model[xarr, yarr, i, 1] = densmantle[row, 2]
                else:
                    model[xarr, yarr, i, 1] = densities[i]
            row += 1

    print 'Calculating load at bottom'
    model[:, :, crustidx, 1] = 0
    load = np.zeros([nx, ny])
    for i in range(nlay):
        load += model[:, :, i, 1]*g*model[:, :, i, 0]

    print 'Calculating density distribution for', crust
    rhocrust = np.zeros([nx, ny])
    rhocrust = -1*(load - targetload)/g/model[:, :, crustidx, 0]
    rhomin = int(np.round(np.min(rhocrust), 0))
    rhomax = int(np.round(np.max(rhocrust), 0))
    print "> Density range:", rhomin, '-', rhomax

    h = "Crustal isostatic density\n"
    h += "Created: " + str(tstart) + "\n"
    h += "Input GMS project: " + str(project) + "\n"
    h += "Input mantle density: " + str(fdensmantle) + "\n"
    h += "Load at model base: " + str(targetloadGPa) + " GPa\n"
    h += "Minimum density: " + str(rhomin) + "\n"
    h += "Maximum density: " + str(rhomax) + "\n"
    h += "Column information:\n"
    h += "0 - X\n"
    h += "1 - Y\n"
    h += "2 - Density / kg/m3"

    print 'Save result to', fout
    np.savetxt(fout, grd2tab(rhocrust, xmin, xmax, ymin, ymax), fmt='%f',
               header=h)