#!/bin/bash
#
# by Christian Meeßen
# christian.meessen@gfz-potsdam.de
# GFZ Potsdam, 2016

if [ $# -lt 2 ]
then
  echo
  echo "Not enough arguments."
  echo
  echo "Usage: ExtractDepthSlice InputFile Depth [PropertyColumn [HeaderLines]]"
  echo "       arguments in [] are optional"
  echo
  echo "Depth          - Depth to extract the values from"
  echo "PropertyColumn - If the InputFile contains multiple columns, this"
  echo "                 defines the order of columns that will be read,"
  echo "                 start counting at 0. Default is 0,1,2"
  echo "HeaderLines    - Number of header lines in input file"
  echo 
  echo "Extracts values from an input file at the given depth."
  echo
  echo "Note that if header lines in the input file start with different"
  echo "characters, i.e. Petrel points with attributes files, you need to define"
  echo "the number of header lines."
  echo
  exit
elif [ $# -eq 2 ]
then
  InFile=$1
  DepthSlice=$2
  column="0,1,2"
  nHeader=""
elif [ $# -eq 3 ]
then
  InFile=$1
  DepthSlice=$2
  column=$3
  nHeader=""
elif [ $# -eq 4 ]
then
  InFile=$1
  DepthSlice=$2
  column=$3
  nHeader="-hi$4"
else
  echo "Input arguments: $#"
fi

echo "Extracting depth slice at z=$DepthSlice from $InFile"
echo "> Extracting columns: $column"
FileOut=$InFile"_"$DepthSlice".dat"
gmt gmtselect $InFile -Z$DepthSlice $nHeader -i$column > $FileOut

rm gmt.history 2> /dev/null

echo "Done."
echo "Output file: $FileOut"
