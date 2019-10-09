"""
List of useful functions
"""

import numpy as np
import sys, os, platform, inspect

class AK135:

    def __init__(self):
        self.data = None
        self.__load_csv__()

    def __load_csv__(self):
        OS = platform.system()
        if OS == 'Windows':
            FolderSep = '\\'
        else:
            FolderSep = '/'
        PyFile = inspect.getfile(inspect.currentframe())
        PyPath = os.path.dirname(os.path.abspath(PyFile))
        ModelFile = PyPath + FolderSep + 'AK135.csv'
        self.data = np.loadtxt(ModelFile, delimiter=';', comments='#')
        self.datacolumns = {
            'depth': 0,
            'density': 1,
            'vp': 2,
            'vs': 3,
            'qkappa': 4,
            'qmu': 5
        }

    def __call__(self, z):
        data = self.data
        depths = data[:, 0]
        values = dict()
        values['density'] = np.interp(z, depths, data[:, 1])
        values['vp'] = np.interp(z, depths, data[:, 2])
        values['vs'] = np.interp(z, depths, data[:, 3])
        values['qkappa'] = np.interp(z, depths, data[:, 4])
        values['qmu'] = np.interp(z, depths, data[:, 5])
        values['pressure'] = self.pressure(z)
        return values

    def pressure(self, z):
        """
        Compute the pressure at depth z by integrating AK135.
        Paramters:

        * z : float
            Depth in km where properties shall be calculated

        Returns:

        * pressure : float
            The pressure at depth z in GPa.
        """
        g = 9.81
        depths = self.data[:, 0]
        depths_sample = np.append(depths[depths < z], z)
        rhos = self.data[:, 1]
        rho_z = np.interp(z, depths, self.data[:, 1])
        rhos_sample = np.append(rhos[0:depths_sample.shape[0]-1], rho_z)
        return g*np.trapz(rhos_sample, depths_sample)/1000.


def read_args():
    """
    How to read and handle command line arguments
    """
    if len(sys.argv) < 2:
      print("Error: not enough arguments!")
      print("Usage: AK135 depth")
      print("\nDepth in km")
      sys.exit()
    try:
        arg1 = float(sys.argv[1])
    except ValueError:
        print("\nError: Input must be point-separated float.\n")
        sys.exit()
    return arg1

def compute(depth):
    """
    Return Pressure from AK135 at given depth.
    Depth range: 18 to 310km
    AK135: http://rses.anu.edu.au/seismology/ak135/ak135f.html

    Parameters:

    * depth : float
        Depth in km where the pressure should be calculated

    Return:

    * Pressure : float
        Pressure at depth in Pa
    """
    model = AK135()
    result = model(depth)
    print()
    print("Depth   : {:10.4f} km  ".format(depth))
    print("Density : {:10.4f} t/m3".format(result['density']))
    print("Vp      : {:10.4f} km/s".format(result['vp']))
    print("Vs      : {:10.4f} km/s".format(result['vs']))
    print("Qkappa  : {:10.4f}     ".format(result['qkappa']))
    print("Qmu     : {:10.4f}     ".format(result['qmu']))
    print("Pressure: {:10.4f} GPa ".format(result['pressure']))
    print()


if __name__ == "__main__":
    compute(read_args())
