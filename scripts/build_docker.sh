docker pull hamzamerzic/meshlab
docker pull nytimes/blender:2.82-gpu-ubuntu18.04
docker build -t joms/opensubdiv:latest --compress opensubdiv
docker build -t joms/cxxopts:latest --compress cxxopts
docker build -t joms/embree:latest --compress embree
docker build -t joms/fbxsdk:latest --compress fbx
docker build -t joms/terra:latest --compress terra
docker build -t joms/nanoflann:latest --compress nanoflann
docker build -t joms/json:latest --compress json
docker build -t joms/optlang:latest --compress Optlang
docker build -t joms/openpose:latest --compress openpose
docker build -t joms/trainer:latest --compress human-model-trainer
