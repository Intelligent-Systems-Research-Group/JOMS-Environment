import sys
experiment_path = sys.argv[1]


from pathlib import Path
import subprocess
basePath = "dataset/scans"
meshlabCommandTemplate = '''docker run --rm \
-v $(pwd)/dataset/poisson:/output \
-v $(pwd)/preprocessing:/root/scripts \
-v $(pwd)/dataset/scans:/scans \
-e IN_DATA=%s  hamzamerzic/meshlab /root/scripts/run_in_meshlab.sh'''

meshlabCommand2Template = '''docker run --rm \
-v $(pwd)/dataset/poisson:/poisson \
-v $(pwd)/preprocessing:/root/scripts \
-v $(pwd)/dataset/scans:/scans \
-e IN_DATA=%s hamzamerzic/meshlab /root/scripts/run_in_meshlab2.sh'''


blenderCommandTemplate = '''docker run --rm -it \
-v %s:/input \
-v %s:/output \
-v $(pwd)/JOMS/template_human/:/template \
-e CAM=/template/%s \
-v %spreprocessing:/blendfiles \
--gpus '"device=1"' nytimes/blender:2.82-gpu-ubuntu18.04 \
bash -c "/blendfiles/run_in_blender.sh"'''

#blenderCommandTemplate = docker run --rm -it \
#-v %sdataset/poisson:/input \
#-v %sdataset/flat_images:/output \
#-v %shuman-model-trainer/template:/config \
#-v %spreprocessing:/blendfiles \
#-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=:0.0 -e XAUTHORITY=~/.Xauthority -e NVIDIA_DRIVER_CAPABILITIES=all \
#--gpus all nytimes/blender:2.82-gpu-ubuntu18.04 \
#bash 

openposeCommandTemplate = '''docker run -it \
-v %s:/images \
-v %s:/output --net=host --gpus '"device=1"' \
joms/openpose:latest ./build/examples/openpose/openpose.bin --display 0 --image_dir=/images/ \
--face --hand --write_json=/output/
'''
#--write_json=/output/
#--write_images=/output/ --face --hand --face_render 1 --hand_render 1 --face_render_threshold 0.001 \
#--write_json=/output/ --face_detector 0

persons = []
suffixes = []
camera_ids = []
camera_paths = ["cameras.json",
	"caesar_cameras.json"]

with open(experiment_path,'r') as f:
	for line in f.readlines():
		if line.startswith("person_ids"):
			persons = [x.strip() for x in line[line.index('=')+1:].split(',')]
		elif line.startswith("person_config_suffixes"):
			suffixes = [x.strip() for x in line[line.index('=')+1:].split(',')]
		elif line.startswith("person_fist"):
			camera_ids = [int(x.strip()) for x in line[line.index('=')+1:].split(',')]
print(persons)
print(suffixes)

#human-model-trainer/person_configs/50002_cluster50f.txt
person_configs_base = Path("JOMS/person_configs")
if False:
	for person,suffix in zip(persons,suffixes):
		person_path = "JOMS/person_configs/%s_%s.txt" % (person,suffix)
		with open(person_path,'r') as f:
			scan_names = ["dataset/scans/"+person+'/'+x.strip()+".xyz" for x in f.readlines()[2:]]
			print(scan_names)
			for scan in scan_names:
				path = Path(scan)
				realPath = path.relative_to(basePath)
				print(realPath)
				input=str(Path("/scans") / path.relative_to(basePath))
				meshlabCommand = meshlabCommandTemplate % input
				process = subprocess.check_call(meshlabCommand, shell=True)
				target = Path("dataset/poisson")/realPath.with_suffix(".ply")
				target.parent.mkdir(parents=True, exist_ok=True)
				Path("dataset/poisson/test.ply").rename(target)

if False:
	for i,person in enumerate(persons):
		s = str(Path.cwd()) + "/"
		s_poisson = str(Path.cwd()/"dataset/poisson"/person)
		print(s_poisson)
		s_output = str(Path.cwd()/"dataset/flat_images"/person)
		(Path.cwd()/"dataset/flat_images"/person).mkdir(parents=True, exist_ok=True)
		blenderCommand = blenderCommandTemplate % (s_poisson,s_output,camera_paths[camera_ids[i]],s)
		print(blenderCommand)
		process = subprocess.check_call(blenderCommand, shell=True)
if True:
	for person in persons:
		openIn = str((Path("dataset/flat_images")/person).absolute())
		openOut = (Path("dataset/pose2d")/person).absolute()
		openOut.mkdir(parents=True, exist_ok=True)
		openposeCommand = openposeCommandTemplate % (openIn,str(openOut))
		print(openposeCommand)
		process = subprocess.check_call(openposeCommand, shell=True)

if False:
    basePath = "dataset/poisson"
    for person,suffix in zip(persons,suffixes):
        person_path = "JOMS/person_configs/%s_%s.txt" % (person,suffix)
        with open(person_path,'r') as f:
            scan_names = ["dataset/poisson/"+person+'/'+x.strip()+".obj" for x in f.readlines()[2:]]
            print(scan_names)
            for scan in scan_names:
                path = Path(scan)
                realPath = path.relative_to(basePath)
                print(realPath)
                input=str(Path("/poisson") / path.relative_to(basePath))
                meshlabCommand = meshlabCommand2Template % input
                print(meshlabCommand)
                process = subprocess.check_call(meshlabCommand, shell=True)
                target = Path("dataset/scans")/realPath.with_suffix(".xyz")
                target.parent.mkdir(parents=True, exist_ok=True)
                Path("dataset/scans/test.xyz").rename(target)
