#!/bin/bash

cd uploaded
latestFile=`ls -rt1 | tail -n 1`
latest_seconds=`stat -c %Y "$latestFile"`
latest=`date -d @$latest_seconds '+%Y-%m-%d %H:%M:%S'`


cd ../upload

parallel_cmd='filename="$(basename {})"; 
random_part=$(mktemp -u XXXXXX); 
suffix=".${filename##*.}"; 
suffix="${suffix%?}";
newname="${filename%.*}-${random_part}${suffix}"; 
ln -sv {} "$newname";'

for i in `cat ../formats.txt`; 
do
  echo -n $i
  find ~/CalibreLibrary/ -type f -iname "*.$i" -newermt "$latest" | parallel --bar $parallel_cmd
done
