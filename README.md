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

