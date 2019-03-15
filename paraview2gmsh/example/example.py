import sys
from collections import OrderedDict
sys.path.append('../')
from paraview2gmsh import process

layers = OrderedDict()
BCs = dict()

layers['Sediments'] = './data/profile0.csv'
layers['Crust'] = './data/profile1.csv'
layers['Mantle'] = './data/profile2.csv'

BCs['Sediments'] = 'upper'
BCs['Mantle'] = 'lower'
lcar = 10e3  # Characteristic length

geo = 'example.geo'

process(layers, BCs, lcar, geo, vscale=10)
