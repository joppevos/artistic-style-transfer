FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
MAINTAINER nagadomi <nagadomi@nurs.or.jp>

SHELL ["/bin/bash", "-c"]

# install deps
RUN apt-get update && apt-get install -y git sudo

# install torch7
RUN git clone https://github.com/nagadomi/distro.git /root/torch --recursive && \
    cd /root/torch && \
     ./install-deps && \
     TORCH_CUDA_ARCH_LIST="Kepler Maxwell Kepler+Tegra Kepler+Tesla Maxwell+Tegra Pascal Volta Turing" ./install.sh -b

RUN apt-get install -y \
    wget \
    libreadline-dev \
    libwebkitgtk-3.0-0

## Install loadcaffe network for Torch
RUN sudo apt-get install -y libprotobuf-dev protobuf-compiler; \
    cd /root/torch && install/bin/luarocks install loadcaffe

# install ffmpeg (required by FAV)
RUN sudo add-apt-repository ppa:jonathonf/ffmpeg-4 && \
    sudo apt-get update && \
    sudo apt-get install -y ffmpeg

# install opencv from source
RUN sudo apt-get install -y \
    build-essential cmake git pkg-config libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev gfortran openexr libatlas-base-dev \
    python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev

RUN mkdir ~/opencv_build && cd ~/opencv_build; \
    git clone https://github.com/opencv/opencv.git; \
    git clone https://github.com/opencv/opencv_contrib.git; \
    cd opencv && git checkout 3.4.2 && cd .. ; \
    cd opencv_contrib && git checkout 3.4.2 && cd ..

RUN cd ~/opencv_build/opencv && mkdir build && cd build; \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON .. ; \
    make -j8 ; \
    sudo make install

# adjusted repo
RUN mkdir /artistic-transfer && \
    git clone https://github.com/joppevos/artistic-style-transfer --recursive /artistic-transfer

# download VGG-19 models
RUN cd /artistic-transfer/models/ && bash download_models.sh

# install flowcode build
RUN cd /artistic-transfer/FlowCode/ && rm -rf build/ ; \
    mkdir build && cd build ; \
    cmake .. ; \
    make

WORKDIR "artistic-transfer/"