# Scripts for Tesseroids

Scripts that make life with [Tesseroids](http://tesseroids.leouieda.com/en/stable/) a bit easier.

## tess2vtu

Converts a tesseroid model to a vtu file that can be opened in ParaView. Written in Python 2.7.

## tesspar

Parallelise the computation of tesseroid models. The model region is subdivided
into smaller sub-regions of which each of the subregions is computed by one
thread. **NOTE:** Requires GMT 5.1, maybe also compatible with later GMT versions.

Tesspar prints a short help when executed without arguments

```
$ tesspar

Not enough arguments.

Usage: tesspar MODEL STATIONS [args]

MODEL          - Tesseroids model
STATIONS       - NetCDF file with station height
-n INT         - Total number of threads
-nx INT        - Number of threads in E-W direction
-ny INT        - Number of threads in N-S direction
-o FILENAME    - Output filename (default gz.dat)
```
