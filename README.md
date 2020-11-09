# JOMS-Environment
Docker Runtime for the paper "Joint Optimization for Multi-Person Shape Models from Markerless 3D-Scans".

A small hello-world example with documentation is provided. A more realistic example for articulated human 3D shape model training is also provided. The documentation for human shape model training well be added in the coming weeks.

## Dependencies
> - docker
> - nvidia-docker
> - git
## Installation
> - git clone this repository
> - ./scripts/download_dependencies.sh
> - download fbx20181_1_fbxsdk_linux and untar the folder into fbx/
> - ./scripts/build_docker.sh
> - building all containers will take some time
## Hello World Example
Start the docker container using
> - ./JOMS/scripts/train_docker.sh

In the docker container, run:

> - source bashrc

Run the hello-world example with

> - ./docker_commands/train_hello_world.sh

After training, exit the container

> - exit

The output is located in output/

## Citation
Please cite these papers in your publications if it helps your research.

Bibtex:
```
@inproceedings{JOMS,
  title={Joint Optimization for Multi-Person Shape Models from Markerless 3D-Scans},
  author={Zeitvogel, Samuel and Dornheim, Johannes and Laubenheimer, Astrid},
  booktitle={European Conference on Computer Vision},
  year={2020}
}
```

## License
JOMS-Environment - excluding the provided models in the weights/ directory - is licensed under the terms of the MIT License.
The trained models located in the weights/ directory are available for free non-commercial use under a different [license](weights/Model_License.pdf). For commercial queries, contact isrg@hs-karlsruhe.de.

To use the docker containers, please check all licenses of the third party libraries and datasets used to build and run the docker containers. In particular, check the license of the project https://github.com/Intelligent-Systems-Research-Group/JOMS.
