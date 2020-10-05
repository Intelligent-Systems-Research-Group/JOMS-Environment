# JOMS-Environment
Docker Runtime for the paper "Joint Optimization for Multi-Person Shape Models from Markerless 3D-Scans".

Only a small hello-world example ist provided. An example for articulated human 3D shape model training will be provided in the coming weeks.

## Dependencies
> - docker
> - nvidia-docker
> - git
## Installation
> - git clone this repository
> - ./scripts/download_dependencies.sh
> - download fbx20181_1_fbxsdk_linux and untar the folder into fbx/
> - ./scripts/build_docker.sh
> - building alle containers will take some time
## Hello World Example
Start the docker container using
> - /JOMS/scripts/train_docker.sh

In the docker container, run:

> - source bashrc

Run the hello-world example with

> - ./docker_commands/train_hello_world.sh

After training, exit the container

> - exit

The output is located in /output
