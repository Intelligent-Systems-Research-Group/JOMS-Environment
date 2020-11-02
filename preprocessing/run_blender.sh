echo $1
docker run --rm -it \
-v $1/dataset/poisson:/input \
-v $1/dataset/flat_images:/output \
-v $1/human-model-trainer/template:/config \
-v $1/preprocessing:/blendfiles \
--gpus all nytimes/blender:2.82-gpu-ubuntu18.04 \
bash -c "/blendfiles/run_in_blender.sh"
#bash
