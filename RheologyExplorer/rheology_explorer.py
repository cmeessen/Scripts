################################################################################
#                     Copyright (C) 2019 by Christian Meessen                  #
#                                                                              #
#                         This file is part of Scripts                         #
#                                                                              #
#        Scripts is free software: you can redistribute it and/or modify       #
#     it under the terms of the GNU General Public License as published by     #
#           the Free Software Foundation version 3 of the License.             #
#                                                                              #
#      GMTScripts is distributed in the hope that it will be useful, but       #
#          WITHOUT ANY WARRANTY; without even the implied warranty of          #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       #
#                   General Public License for more details.                   #
#                                                                              #
#      You should have received a copy of the GNU General Public License       #
#       along with Scripts. If not, see <http://www.gnu.org/licenses/>.        #
################################################################################
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def materials():
    """
    Contains a list of materials used for strength computation with exodus
    module. Available properties are

    Meta properties
    ---------------
    name : str
        Name of the material
    altname : str
        Alternative name
    source : str
        Data source
    via : str
        Where this data has been used

    Byerlee's law
    -------------
    f_f_e : float
        Friction coefficient for extension
    f_f_c : float
        Friction coefficient for compression
    f_p : float
        Pore fluid factor
    rho_b : float
        Bulkd density of the rock / kg/m3

    Dislocation creep
    -----------------
    a_p : float
        Preexponential scaling factor / Pa^(-n)/s
    n : float
        Power law exponent
    q_p : float
        Activation energy / J/mol

    Diffusion creep
    ---------------
    a_f : float
        Preexponential scaling factor / 1/Pa/s
    q_f : float
        Activation energy / J/mol
    a : float
        Grain size / m
    m : float
        Grain size exponent

    Dorn's law creep
    ----------------
    sigma_d : float
        Dorn's law stress / Pa
    q_d : float
        Dorn's law activation energy / J/mol
    a_d : float
        Dorn's law strain rate
    """
    """
    Template

    r.append(dict(name='',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=,  # Bulk density
                    # Dislocation creep
                    a_p=,   # Preexponential scaling factor / Pa^(-n)/s
                    n=,         # Power law exponent
                    q_p=,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    """
    def AGPa(A,n):
        A = float(A)
        n = float(n)
        return A*10.0**(-1.0*n*9.0)

    r = list()
    r.append(dict(name='olivine',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=3300.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(4e15,3.0),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.0,         # Power law exponent
                    q_p=540.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='diabase',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2950.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(3.2e6,3.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.4,         # Power law exponent
                    q_p=260.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='quartz_diorite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2900.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(2e4,2.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=219.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='anorthosite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2800.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(1.3e6,3.2),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.2,         # Power law exponent
                    q_p=238.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='albite_rock',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2600.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(1.3e6,3.9),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.9,         # Power law exponent
                    q_p=234.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='quartzite_wet',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(2e3, 2.3),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.3,         # Power law exponent
                    q_p=154.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='quartzite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(100,2.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=156.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='granite_wet',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(100,2.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=156.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='granite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='Ranalli and Murpy (1987)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(5,3.2),     # Preexponential scaling factor / Pa^(-n)/s
                    n=3.2,         # Power law exponent
                    q_p=123.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    r.append(dict(name='olivine_dry',
                    altname='Mantle',
                    source='Goetze and Evans (1979)',
                    source_disloc='Goetze and Evans (1979)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=3300.0,  # Bulk density
                    # Dislocation creep
                    a_p=7.0e-14,   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.0,         # Power law exponent
                    q_p=510.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=8.5e9, # Dorn's law stress
                    q_d=535e3,     # Dorn's law activation energy
                    a_d=5.7e11))   # Dorn's law strain rate / 1/s
    r.append(dict(name='mafic_granulite',
                    altname='Mafic granulites',
                    source='Wilks and Carter (1990)',
                    source_disloc='Wilks and Carter (1990)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=3050.0,  # Bulk density
                    # Dislocation creep
                    a_p=8.83e-22,  # Preexponential scaling factor / Pa^(-n)/s
                    n=4.2,         # Power law exponent
                    q_p=445.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None,  # Dorn's law stress
                    q_d=None,      # Dorn's law activation energy
                    a_d=None))     # Dorn's law strain rate
    r.append(dict(name='diabase_dry',
                    altname='Gabbroid rocks',
                    source='Carter and Tsenn (1987)',
                    source_disloc='Carter and Tsenn (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2920.0,  # Bulk density
                    # Dislocation creep
                    a_p=6.31e-20,  # Preexponential scaling factor / Pa^(-n)/s
                    n=3.05,        # Power law exponent
                    q_p=276.0e3,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None,  # Dorn's law stress
                    q_d=None,      # Dorn's law activation energy
                    a_d=None))     # Dorn's law strain rate
    r.append(dict(name='granite_dry',
                    altname='Meta-sedimentary rocks',
                    source='Carter and Tsenn (1987)',
                    source_disloc='Carter and Tsenn (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2750.0,  # Bulk density
                    # Dislocation creep
                    a_p=3.16e-26,  # Preexponential scaling factor / Pa^(-n)/s
                    n=3.3,         # Power law exponent
                    q_p=186e3,     # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None,  # Dorn's law stress
                    q_d=None,      # Dorn's law activation energy
                    a_d=None))     # Dorn's law strain rate
    r.append(dict(name='quartzite_dry',
                    altname='Sediments',
                    source='Burov et al. (1998)',
                    source_disloc='Burov et al. (1998)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016), Carter and Tsenn (1987)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2600,    # Bulk density
                    # Dislocation creep
                    a_p=5.0e-12,   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.0,         # Power law exponent
                    q_p=190e3,     # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None,  # Dorn's law stress
                    q_d=None,      # Dorn's law activation energy
                    a_d=None))     # Dorn's law strain rate
    r.append(dict(name='diorite_dry',
                    altname='Meta-igneous rocks',
                    source='Burov et al. (1998)',
                    source_disloc='Burov et al. (1998)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2800,  # Bulk density
                    # Dislocation creep
                    a_p=5.2e-18,     # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=219e3,     # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None,  # Dorn's law stress
                    q_d=None,      # Dorn's law activation energy
                    a_d=None))     # Dorn's law strain rate
    r.append(dict(name='peridotite_dry',
                    altname='Mantle lithosphere of slab and shield, \
                             dry_olivine',
                    source='Hirth and Kohlstedt (1996), Kameyama et al. (1999)',
                    source_disloc='Hirth and Kohlstedt (1996)',
                    source_diff='Kameyama et al. (1999)',
                    source_dorn='Kameyama et al. (1999)',
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=3280.0,     # Bulk density
                    # Dislocation creep
                    a_p=5.011e-17,    # Preexponential scaling factor, -16.3
                    n=3.5,            # Power law exponent
                    q_p=535e3,        # Activation energy
                    # Diffusion creep
                    a_f=2.570e-11,    # Preexp. scaling factor / 1/Pa/s, -10.59
                    q_f=300e3,        # Activation energy / J/mol
                    a=0.1e-3,         # Grain size / m
                    m=2.5,            # Grain size exponent
                    # Dorn's law
                    sigma_d=8.5e9,    # Dorn's law stress / Pa
                    q_d=535e3,        # Dorn's law activation energy / J/mol
                    a_d=5.754e11))     # Dorn's law strain rate
    r.append(dict(name='peridotite_dry_SA',
                    altname='Mantle lithosphere of South America, not shield',
                    source='Hirth and Kohlstedt (1996), Kameyama et al. (1999)',
                    source_disloc='Hirth and Kohlstedt (1996)',
                    source_diff='Kameyama et al. (1999)',
                    source_dorn='Kameyama et al. (1999)',
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=3280.0,     # Bulk density
                    # Dislocation creep
                    a_p=5.002e-15,      # Preexponential scaling factor
                    n=3.5,            # Power law exponent
                    q_p=515e3,        # Activation energy
                    # Diffusion creep
                    a_f=2.570e-11,     # Preexp. scaling factor / 1/Pa/s
                    q_f=300e3,        # Activation energy / J/mol
                    a=0.1e-3,         # Grain size / m
                    m=2.5,            # Grain size exponent
                    # Dorn's law
                    sigma_d=8.5e9,    # Dorn's law stress / Pa
                    q_d=535e3,        # Dorn's law activation energy / J/mol
                    a_d=5.754e11))     # Dorn's law strain rate
    r.append(dict(name='peridotite_dry_asthenosphere',
    # Difference to peridotite_dry_SA is density
                    altname='Mantle asthenosphere',
                    source='Hirth and Kohlstedt (1996), Kameyama et al. (1999)',
                    source_disloc='Hirth and Kohlstedt (1996)',
                    source_diff='Kameyama et al. (1999)',
                    source_dorn='Kameyama et al. (1999)',
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=3300.0,     # Bulk density
                    # Dislocation creep
                    a_p=5.012e-15,      # Preexponential scaling factor
                    n=3.5,            # Power law exponent
                    q_p=515e3,        # Activation energy
                    # Diffusion creep
                    a_f=2.570e-11,     # Preexp. scaling factor / 1/Pa/s
                    q_f=300e3,        # Activation energy / J/mol
                    a=0.1e-3,         # Grain size / m
                    m=2.5,            # Grain size exponent
                    # Dorn's law
                    sigma_d=8.5e9,    # Dorn's law stress / Pa
                    q_d=535e3,        # Dorn's law activation energy / J/mol
                    a_d=5.754e11))     # Dorn's law strain rate
    r.append(dict(name='quartzite_wet_2650',
                    altname='sediments',
                    source='Gleason and Tullis (1995)',
                    source_disloc='Gleason and Tullis (1995)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2650.0,     # Bulk density
                    # Dislocation creep
                    a_p=1e-28,        # Preexponential scaling factor
                    n=4.0,            # Power law exponent
                    q_p=223e3,        # Activation energy
                    # Diffusion creep
                    a_f=None,         # Preexp. scaling factor / 1/Pa/s
                    q_f=None,         # Activation energy / J/mol
                    a=None,           # Grain size / m
                    m=None,           # Grain size exponent
                    # Dorn's law
                    sigma_d=None,     # Dorn's law stress
                    q_d=None,         # Dorn's law activation energy
                    a_d=None))        # Dorn's law strain rate
    r.append(dict(name='quartzite_wet_2700',
                    altname='Uppermost crust continent',
                    source='Gleason and Tullis (1995)',
                    source_disloc='Gleason and Tullis (1995)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2700.0,     # Bulk density
                    # Dislocation creep
                    a_p=1e-28,        # Preexponential scaling factor
                    n=4.0,            # Power law exponent
                    q_p=223e3,        # Activation energy
                    # Diffusion creep
                    a_f=None,         # Preexp. scaling factor / 1/Pa/s
                    q_f=None,         # Activation energy / J/mol
                    a=None,           # Grain size / m
                    m=None,           # Grain size exponent
                    # Dorn's law
                    sigma_d=None,     # Dorn's law stress
                    q_d=None,         # Dorn's law activation energy
                    a_d=None))        # Dorn's law strain rate
    r.append(dict(name='quartzite_wet_weak',
                    altname='Upper crust continent',
                    source='Gleason and Tullis (1995)',
                    source_disloc='Gleason and Tullis (1995)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2800.0,     # Bulk density
                    # Dislocation creep
                    a_p=1e-27,        # Preexponential scaling factor
                    n=4.0,            # Power law exponent
                    q_p=223e3,        # Activation energy
                    # Diffusion creep
                    a_f=None,         # Preexp. scaling factor / 1/Pa/s
                    q_f=None,         # Activation energy / J/mol
                    a=None,           # Grain size / m
                    m=None,           # Grain size exponent
                    # Dorn's law
                    sigma_d=None,     # Dorn's law stress
                    q_d=None,         # Dorn's law activation energy
                    a_d=None))        # Dorn's law strain rate
    r.append(dict(name='plagioclase_wet',
    # Note: this one doesn't fit with the model parameters given in drezina.inp!
                    altname='Granulite, mafic crust continent',
                    source='Rybacki and Dresen (2000)',
                    source_disloc='Rybacki and Dresen (2000)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2950.0,     # Bulk density
                    # Dislocation creep
                    a_p=3.981e-16,      # Preexponential scaling factor
                    n=3.0,            # Power law exponent
                    q_p=356e3,        # Activation energy
                    # Diffusion creep
                    a_f=None,         # Preexp. scaling factor / 1/Pa/s
                    q_f=None,         # Activation energy / J/mol
                    a=None,           # Grain size / m
                    m=None,           # Grain size exponent
                    # Dorn's law
                    sigma_d=None,     # Dorn's law stress
                    q_d=None,         # Dorn's law activation energy
                    a_d=None))        # Dorn's law strain rate
    r.append(dict(name='granulite_dry',
                    altname='Pikwetonian granulite',
                    source='UNKNOWN',
                    source_disloc='UNKNOWN',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006) Drezina.inp',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=3.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2950,       # Bulk density
                    # Dislocation creep
                    a_p=3.2e-21,      # Preexponential scaling factor
                    n=4.2,            # Power law exponent
                    q_p=445.0e3,      # Activation energy
                    # Diffusion creep
                    a_f=None,         # Preexp. scaling factor / 1/Pa/s
                    q_f=None,         # Activation energy / J/mol
                    a=None,           # Grain size / m
                    m=None,           # Grain size exponent
                    # Dorn's law
                    sigma_d=None,     # Dorn's law stress
                    q_d=None,         # Dorn's law activation energy
                    a_d=None))        # Dorn's law strain rate
    return r


def sigma_byerlee(material, z, mode):
    """
    Compute the byerlee differential stress. Requires the material
    properties friction coefficient (f_f), pore fluid factor (f_p) and
    the bulk density (rho_b).

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. The
        required keys are 'f_f_e', 'f_f_c', 'f_p' and 'rho_b'
    z : float
        Depth below surface in m
    mode : str
        'compression' or 'extension'

    Returns
    -------
        sigma_d : float
    """
    if mode == 'compression':
        f_f = material['f_f_c']
    elif mode == 'extension':
        f_f = material['f_f_e']
    else:
        raise ValueError('Invalid parameter for mode:', mode)
    f_p = material['f_p']
    rho_b = material['rho_b']
    g = 9.81  # m/s2
    return f_f*rho_b*g*z*(1.0 - f_p)

def sigma_diffusion(material, temp, strain_rate):
    """
    Computes differential stress for diffusion creept at specified
    temperature and strain rate. Material properties require grain size 'd',
    grain size exponent 'm', preexponential scaling factor for diffusion
    creep 'a_f', and activation energy 'q_f'.

    For diffusion creep, n=1.

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. Required
        keys are 'd', 'm', 'a_f', 'q_f'
    temp : float
        Temperature in Kelvin
    strain_rate : float
        Reference strain rate in 1/s

    Returns
    -------
        sigma_diffusion : float
    """
    R = 8.314472 #m2kg/s2/K/mol
    d = material['d']
    m = material['m']
    a_f = material['a_f']
    q_f = material['q_f']
    if a_f is None:
        return np.nan
    else:
        return d**m*strain_rate/a_f*np.exp(q_f/R/temp)

def sigma_dislocation(material, temp, strain_rate):
    """
    Compute differential stress envelope for dislocation creep at
    certain temeprature and strain rate. Requires preexponential scaling
    factor 'a_p', power law exponent 'n' and activation energy 'q_p'.

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. Required
        keys are 'a_p', 'n' and 'q_p'
    temp : float
        Temperature in Kelvin
    strain_rate : float
        Reference strain rate in 1/s

    Returns
    -------
        sigma_d : float
    """
    R = 8.314472 # m2kg/s2/K/mol
    a_p = material['a_p']
    n = material['n']
    q_p = material['q_p']
    return (strain_rate/a_p)**(1.0/n)*np.exp(q_p/n/R/temp)

def sigma_dorn(material, temp, strain_rate):
    """
    Compute differential stress for solid state creep with Dorn's law.
    Requires Dorn's law stress 'sigma_d', Dorn's law activation energy
    'q_d' and Dorn's law strain rate 'A_p'.

    Dorn's creep is a special case of Peierl's creep with q=2

    sigma_delta = sigma_d*(1-(-R*T/Q*ln(strain_rate/A_d))^(1/q))

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. Required
        keys are 'sigma_d', 'q_d' and 'A_p'
    temp : float
        Temperature in Kelvin
    strain_rate : float
        Reference strain rate in 1/s

    Returns
    -------
        sigma_d : float
    """
    R = 8.314472 # m2kg/s2/K/mol
    sigma_d = material['sigma_d']
    q_d = material['q_d']
    a_d = material['a_d']
    if sigma_d is None:
        return np.nan
    else:
        return sigma_d*(1.0 - np.sqrt(-1.0*R*temp/q_d*np.log(strain_rate/a_d)))

def sigma_d(material, z, temp, strain_rate=None,
            compute=None, mode=None):
    """
    Computes differential stress for a material at given depth, temperature
    and strain rate. Returns the minimum of Byerlee's law, dislocation creep
    or dorn's creep.

    Parametersq
    ----------
    material : dict
        Dict containing material properties required by sigma_byerlee() and
        sigma_dislocation()
    z : float
        Positive depth im m below surface
    temp : float
        Temperature in K
    strain_rate : float
        Reference strain rate in 1/s. If `None` will use self.strain_rate
    compute : list
        List of processes to compute: 'dislocation', 'diffusion', 'dorn'.
        Default is ['dislocation', 'dorn'].
    mode : str
        'compression' or 'extension'

    Returns
    -------
    Sigma : float
        Differential stress in Pa
    """
    if z < 0:
        raise ValueError('Depth must be positive. Got z =', z)
    if strain_rate is None:
        e_prime = self.strain_rate
    else:
        e_prime = strain_rate

    compute_default = ['dislocation', 'dorn']
    if compute is None:
        compute = compute_default
    else:
        # Check the keywords
        for kwd in compute:
            if kwd not in compute_default:
                raise ValueError('Unknown compute keyword', kwd)

    s_byerlee = sigma_byerlee(material, z, mode)

    if 'diffusion' in compute:
        s_diff = sigma_diffusion(material, temp, e_prime)
    else:
        s_diff = np.nan

    if 'dislocation' in compute and 'dorn' in compute:
        if s_byerlee > 200e6:
            s_creep = sigma_dislocation(material, temp, e_prime)
        else:
            s_creep = sigma_dorn(material, temp, e_prime)
    elif 'dislocation' in compute and not 'dorn' in compute:
        s_creep = sigma_dislocation(material, temp, e_prime)
    elif 'dorn' in compute and not 'dislocation' in compute:
        s_creep = sigma_dorn(material, temp, e_prime)
    else:
        s_creep = np.nan

    return min([s_byerlee, s_creep, s_diff])

def print_mat_info(mat, ax=None):
    # make a pretty info plot on the materials
    print ''
    print '###################################################################'
    print 'Name             :', mat['name']
    print 'Alternative name :', mat['altname']
    print 'Sources          :', mat['source']
    print 'Used in          :', mat['via']
    print ''
    print 'Byerlee\'s law properties'
    print 'f_f     :', mat['f_f_e'], '/', mat['f_f_c']
    print 'f_p     :', mat['f_p']
    print 'rho_b   :', mat['rho_b']
    print ''
    print 'Dislocation creep properties'
    print 'Source  :', mat['source_disloc']
    print 'A_p     :', mat['a_p']
    print 'n       :', mat['n']
    print 'Q_p     :', mat['q_p']
    if not mat['a_f'] is None:
        print ''
        print 'Diffusion creep properties'
        print 'Source  :', mat['source_diff']
        print 'A_f     :', mat['a_f']
        print 'Q_f     :', mat['q_f']
        print 'a       :', mat['a']
        print 'm       :', mat['m']
    if not mat['sigma_d'] is None:
        print ''
        print 'Dorn\'s law properties'
        print 'Source:', mat['source_dorn']
        print 'sigma_d :', mat['sigma_d']
        print 'Q_d     :', mat['q_d']
        print 'A_d     :', mat['a_d']
    print '###################################################################'
    print ''
    if ax:
        props_byerlee = ['f_f_e', 'f_f_c', 'f_p', 'rho_b']
        props_disloc = ['source_disloc', 'a_p', 'n', 'q_p']
        props_diff = ['source_diff', 'a_f', 'q_f', 'a', 'm']
        props_dorn = ['source_dorn', 'sigma_d', 'q_d', 'a_d']
        row_labels = ['name', 'source', 'via']
        row_labels.extend(props_byerlee)
        row_labels.extend(props_disloc)
        if not mat['a_f'] is None:
            row_labels.extend(props_diff)
        if not mat['sigma_d'] is None:
            row_labels.extend(props_dorn)
        cell_text = []
        for prop in row_labels:
            cell_text.append([mat[prop]])
        thetable = ax.table(cellText=cell_text,
                             cellColours=None,
                             cellLoc='right',
                             colWidths=None,
                             rowLabels=row_labels,
                             rowColours=None,
                             rowLoc='Left',
                             colLabels=None,
                             colColours=None,
                             colLoc='center',
                             #loc='center',
                             bbox=(0, 0, 1, 1))
        thetable.auto_set_font_size(False)
        thetable.set_fontsize('small')
        return thetable

def compute_dsigma(mat, z, T, strain_rate):
    """
    Compute differential stress for a given material at depths z and
    temperatures T. Comptues for both compression and extension and
    therefore the output depths array is a concatenation of z:z[::-1].

    Parameters
    ----------
    mat : dict
        Dict of type as defined in def materials()
    z : np.array
        1D array of increasing depth values in positive m
    T : np.array
        1D array of same shape as z with T in Kelvin
    strain_rate : float
        Strain rate in 1/s

    Returns
    -------
    dsigma : np.array
        1D array with computed differential stress.
    depths : np.array
        1D array with corresponding depth values
    """
    s_d_c = np.empty_like(z)              # Diff. stress for compression
    s_d_e = np.empty_like(z)              # Diff. stress for extension
    for i in range(z.shape[0]):
        s_d_c[i] = -1*sigma_d(mat, z[i], T[i], strain_rate=strain_rate,
                              mode='compression')
        s_d_e[i] = sigma_d(mat, z[i], T[i], strain_rate=strain_rate,
                           mode='extension')
    dsigma = np.concatenate((s_d_c, s_d_e[::-1]))
    depths = np.concatenate((z, z[::-1]))
    return dsigma, depths

if __name__ == "__main__":
    mat_dbase = sorted(materials(), key=lambda k:k['name'] )

    geotherm = np.loadtxt('./McKenzieetal2005_Fig4_Geotherm.csv',
                          skiprows=1, delimiter=',')
    geotherm[:, 0] *= 1000
    geotherm[:, 1] += 273

    strain_rate = 1e-16
    num_points = 1000

    xmin = -4.5
    xmax = 1.5

    ymax = 100.0   # Max. depth in km
    ymin = 0.0     # Min. depth in km

    zs = np.linspace(0, ymax*1000, num=num_points)
    T = np.interp(zs, geotherm[:,0], geotherm[:,1])

    import matplotlib.gridspec as gridspec
    gs = gridspec.GridSpec(1, 2)

    #fig = plt.figure(figsize=(8,10), tight_layout=True)
    fig = plt.figure()
    gs0 = gridspec.GridSpec(1,2, width_ratios=[1,1])
    gs0left = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs0[0])
    gs0right = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[1],
                                                height_ratios=[1,0.9])

    ax = plt.Subplot(fig, gs0left[0])
    fig.add_subplot(ax)
    ax2 = ax.twiny()

    ax_table = plt.Subplot(fig, gs0right[1])
    ax_table.set_axis_off()
    fig.add_subplot(ax_table)

    labels = []
    lines = []
    matlist = []
    labeld = dict()

    # Plot a vertical line at 0GPa
    ax.plot([0,0], [ymin, ymax], lw=1, c='black', alpha=0.5)

    n=0 # For colours
    nmax=len(mat_dbase)
    for mat in mat_dbase:
        matlist.append(mat)
        label = mat['name'] + ', ' + mat['source']
        labeld[label] = n
        c = plt.cm.nipy_spectral(n*1.0/nmax)   # Colour index
        sigma_plot, z_plot = compute_dsigma(mat, zs, T, strain_rate)
        lines.append(ax.plot(sigma_plot/1e9, z_plot/1000, label=label, c=c)[0])
        n+=1

    ax.set_xlabel('Strength / GPa')
    ax.set_ylabel('Depth / km')
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymax, ymin)

    ax2.plot(T-273, zs/1000, linestyle="--")
    ax2.set_xlabel('Temperature / $^\circ$C')
    ax2.set_xlim(0,1350)

    leg = ax.legend(loc='upper left', bbox_to_anchor=(1,1),
                    prop={'size': 'small'},
                    title='Click on the line to toggle visibility')

    # Make the buttons and input box
    def submit(text):
        strain_rate = float(text)
        print 'Recomputing strength for strain rate', strain_rate
        for i in range(len(lines)):
            mat = matlist[i]
            sigma_plot, z_plot = compute_dsigma(mat, zs, T, strain_rate)
            lines[i].set_xdata(sigma_plot*1e-9)
        plt.draw()
    axbox = plt.axes([0.8, 0.8, 0.1, 0.05])
    text_box = mpl.widgets.TextBox(axbox, 'Strain rate', initial='1e-16')
    text_box.on_submit(submit)
    # Make a toggle all on button
    def toggle_all_on(event):
        for legline, origline in zip(leg.get_lines(), lines):
            origline.set_visible(True)
            legline.set_alpha(1.0)
        fig.canvas.draw()
    ax_all_on = plt.axes([0.8, 0.75, 0.1, 0.05])
    button_all_on = mpl.widgets.Button(ax_all_on, 'Show all')
    button_all_on.on_clicked(toggle_all_on)
    # Toggle all off button
    def toggle_all_off(event):
        for legline, origline in zip(leg.get_lines(), lines):
            origline.set_visible(False)
            legline.set_alpha(0.2)
        fig.canvas.draw()
    ax_all_off = plt.axes([0.8, 0.7, 0.1, 0.05])
    button_all_off = mpl.widgets.Button(ax_all_off, 'Hide all')
    button_all_off.on_clicked(toggle_all_off)
    # Toggle axes grid on
    def toggle_axes_grid_on(event):
        ax.grid(which='both', axis='both', alpha=0.5)
        fig.canvas.draw()
    ax_grid_on = plt.axes([0.8, 0.65, 0.1, 0.05])
    button_grid_on = mpl.widgets.Button(ax_grid_on, 'Grid on')
    button_grid_on.on_clicked(toggle_axes_grid_on)
    # Toggle axes grid off
    def toggle_axes_grid_off(event):
        ax.grid(False)
        fig.canvas.draw()
    ax_grid_off = plt.axes([0.8, 0.60, 0.1, 0.05])
    button_grid_off = mpl.widgets.Button(ax_grid_off, 'Grid off')
    button_grid_off.on_clicked(toggle_axes_grid_off)
    # Toggle compression/extension
    def toggle_compression_extension(event):
        ax.set_xlim(xmin, xmax)
        fig.canvas.draw()
    ax_comp_ext = plt.axes([0.8, 0.55, 0.1, 0.05])
    button_comp_ext = mpl.widgets.Button(ax_comp_ext, 'Comp. and ext.')
    button_comp_ext.on_clicked(toggle_compression_extension)
    # Only Compression
    def toggle_compression(event):
        ax.set_xlim(xmin, 0)
        fig.canvas.draw()
    ax_comp = plt.axes([0.8, 0.5, 0.1, 0.05])
    button_comp = mpl.widgets.Button(ax_comp, 'Only compression')
    button_comp.on_clicked(toggle_compression)
    # Only extension
    def toggle_extension(event):
        ax.set_xlim(0, xmax)
        fig.canvas.draw()
    ax_ext = plt.axes([0.8, 0.45, 0.1, 0.05])
    button_ext = mpl.widgets.Button(ax_ext, 'Only extension')
    button_ext.on_clicked(toggle_extension)

    # Make the clickable legend
    # legline - the line object in the legend
    # origline - the line object in the plot window
    lined = dict()
    for legline, origline in zip(leg.get_lines(), lines):
        legline_width=8
        legline_picker=int(0.5*legline_width)
        legline.set_linewidth(legline_width)
        legline.set_picker(legline_picker) # 5pts tolerance
        lined[legline] = origline
        origline.set_visible(False)
        legline.set_alpha(0.2)

    def onpick_legend(event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        global the_table
        legline = event.artist
        origline = lined[legline]
        vis = not origline.get_visible()
        origline.set_visible(vis)
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
        if vis:
            legline.set_alpha(1.0)
            # Also print info
            mat_idx = labeld[origline.get_label()]
            if 'the_table' in globals():
                print 'deleting table'
                the_table.remove()
                del the_table
                fig.canvas.draw()
            the_table = print_mat_info(mat_dbase[mat_idx], ax_table)
        else:
            if 'the_table' in globals():
                print 'deleting table'
                the_table.remove()
                del the_table
                fig.canvas.draw()
            legline.set_alpha(0.2)
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', onpick_legend)
    fig.canvas.set_window_title('Rheology explorer')
    plt.subplots_adjust(top=0.925,
                        bottom=0.07,
                        left=0.065,
                        right=0.75,
                        hspace=0.2,
                        wspace=0.2)
    # If manager is wxmanager
    #mng = plt.get_current_fig_manager()
    #mng.frame.Maximize(True)
    # For QT
    #figManager = plt.get_current_fig_manager()
    #figManager.window.showMaximized()
    plt.show()
