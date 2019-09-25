#!/usr/bin/env bash

filename=sloppiejoppie
foldername=flow_default/
startframe=${3:-1}
#stepsize=${4:-1}

cd sloppiejoppie/
#cd ${filename}/
# add all images in an array
array=(*.ppm)
mkdir -p "${foldername}"
cd ..
# cut frame number of image
i=$((startframe + 1))

while true; do
  if [ -f "${array[$i]}" ]; then
  ./FlowCode/build/deepflow_opencv \
    --gpu \
    /artistic-transfer/"${filename}"/"${array[$i]}" \
    /artistic-transfer/"${filename}"/"${array[(($i + 1))]}" \
    /artistic-transfer/"${foldername}"/frame_"$i".flo
  else
    echo "finished flow"
    break
  fi

  i=$(( $i + 1))
done
