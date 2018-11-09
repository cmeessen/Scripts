 #!/bin/bash

 for f in ./*
 do
   if [ "$f" != "convert.sh" ]
   then
     sed -i 's/ps2raster/ps2raster/g' $f
   fi
 done
