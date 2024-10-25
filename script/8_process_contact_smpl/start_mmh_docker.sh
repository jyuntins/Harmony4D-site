cd ../..

### rand a 5 digit port number
function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(($RANDOM+1000000000))
    echo $(($num%$max+$min))
}

###----------------------------------------------------------
DOCKER_CONTAINER_NAME='mmhuman3d'
TAG='latest'

PORT=$(rand 10000 20000)

DATE_WITH_TIME=`date "+%Y%m%d-%H%M%S"`
RUN_NAME="$(echo "mmhuman3d_${DATE_WITH_TIME}")"

# ###----------------------------------------------------------
DOCKER_REGISTRY='rawalkhirodkar'
DOCKER_CONTAINER="$(echo "${DOCKER_REGISTRY}/${DOCKER_CONTAINER_NAME}:${TAG}")"


###----------------------------------------------------------
# USERNAME=$(whoami)
USERNAME='rawalk'
ROOT_DIR="$(echo "/home/${USERNAME}")"
WORK_DIR="$(echo "/home/${USERNAME}/Desktop/ego/ego_exo/scripts/8_process_contact_smpl")" ## /home/rawalk on DGX and /home/ubuntu on AWS
ROOT_DIR_MOUNT="$(echo "${ROOT_DIR}:${ROOT_DIR}:Z")"

###------------------------------------------------------------------
sudo docker run --privileged -it --rm --ipc=host --name=${RUN_NAME} \
		--net=host \
		--cap-add SYS_ADMIN -u 0 \
		-p ${PORT}:${PORT} \
		--env="DISPLAY" \
    	--env="QT_X11_NO_MITSHM=1" \
    	--userns="host" \
    	--runtime=nvidia \
    	-e XAUTHORITY -e NVIDIA_DRIVER_CAPABILITIES=all \
		-e DISPLAY=$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-w ${WORK_DIR} \
		-v ${ROOT_DIR_MOUNT} \
		-v "/mnt:/mnt:Z" \
		-v "/media:/media:Z" \
		${DOCKER_CONTAINER} /bin/bash

