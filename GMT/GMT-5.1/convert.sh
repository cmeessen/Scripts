 #!/bin/bash
################################################################################
#                     Copyright (C) 2017 by Christian Meeßen                   #
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

 for f in ./*
 do
   if [ "$f" != "convert.sh" ]
   then
     sed -i 's/ps2raster/ps2raster/g' $f
   fi
 done
