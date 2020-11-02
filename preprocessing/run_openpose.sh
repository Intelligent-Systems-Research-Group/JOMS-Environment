#docker run -it -v /media/caduser/data/caesar_convert/images/:/images -v /media/caduser/data/caesar_convert/openpose/:/output --net=host -e NVIDIA_VISIBLE_DEVICES=3 --runtime=nvidia iz-gitlab-01.hs-karlsruhe.de:4567/isrg/docker-images/openpose:2.0 ./build/examples/openpose/openpose.bin --display 0 --image_dir="/images/csr4096a/" --write_images="/output/" --write_json="/output/" --face --hand
docker run -it -v /media/dl/Data/hyperdocker/hyperdocker/dataset/flat_images/:/images -v /media/dl/Data/hyperdocker/hyperdocker/dataset/pose2d:/output --net=host -e NVIDIA_VISIBLE_DEVICES=0 --gpus all hypermod/openpose:latest ./build/examples/openpose/openpose.bin --display 0 --image_dir="/images/" --write_images="/output/" --write_json="/output/" --face --hand