Aristic-Video with OpenCV and Torch

### Getting started
#### Setup
Tested on Ubuntu 18.04

- Install Nvidia drivers
- Install Docker

#### Installation
- build the docker image (size of 20gb)
``` 
docker run --gpus=all -v`pwd`:/data --rm -it vosser/artistic-video:latest
```
\`pwd\` will mount the directory where you run it from to the folder /data in the container. Your style transfer material should be here located (images, video). If you would like to to mount a different location you replace \`pwd\` with the desired path.

- Inside the container, run the following command.
```
./stylizeVideo.sh /data/<name_of_video> /data/<name_of_style_image> 
```
The images can be found inside the folder named <name_of_video>
##### recommended
Optional is giving the third argument to export it directly to the mount of the container to be able to see the output. 
```
./stylizeVideo.sh /data/<name_of_video> /data/<name_of_style_image> /data/<output_folder_name>
```
To display the \*.png files run ```xdg-open out-0001.png```


#### More info
the official repo from artistic-video: https://github.com/manuelruder/artistic-videos
