#!/usr/bin/env bash

filename=$1
foldername=$2
startframe=${3:-1}
#stepsize=${4:-1}

cd ${filename}/

# get the lastest file
IMAGES=$(ls -t)
i=$((startframe + 1))

MAX_FRAME=$(ls -t | head -1 | tr "." "\n" | head -1 | tr "-" "\n" | tail -1)
MAX_FRAME=$(($MAX_FRAME + 0))
array=(*.ppm)

mkdir -p "${foldername}"

# cut frame number of image
i=$startframe
while [ "$i" -le $MAX_FRAME ]; do
  ~/apps/FlowCode/build/deepflow_opencv \
    --gpu \
    /artistic-transfer/surf_input/"${array[$i]}" \
    /artistic-transfer/surf_input/"${array[(($i + 1))]}" \
    /artistic-transfer/"${foldername}/{$i}".flo

  i=$(( "$i" + 1))
done
