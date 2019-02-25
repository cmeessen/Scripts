#!/bin/bash

echo "Start"
GMSProfile CPB3_T_ascii.fem 200000 7200000 1000000 6800000 -u S20 -vox Vs_Assumpcaoetal2013_UTM20_NN_OnCratonic.dat,3 -voxt V@-s@-_/_km/s -ve 2
