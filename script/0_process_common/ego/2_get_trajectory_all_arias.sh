cd ../..

# https://docs.google.com/document/d/11NLILsZ25n057ZxjLhzl9FtDmlQWe7i9WkctMQsMFKM/edit#

###------------------------lego--------------------------------------
VRS_FILE='/home/rawalk/Desktop/datasets/ego_exo/common/raw_from_cameras/basketball/aria01/recording/video.vrs'
OUTPUT_DIR='/home/rawalk/Desktop/datasets/ego_exo/common/raw_from_cameras/basketball/aria01/recording/alignment'

###----------------------------------------------------------------------------------------------
OUTPUT_DIR=${OUTPUT_DIR}_temple3 ## main folder for output dump

rm -rf ${OUTPUT_DIR}
mkdir -p ${OUTPUT_DIR}

###----------------------------------------------------------------------------------------------
##----cd to fbsource----
cd ~/fbsource
buck run @arvr/mode/linux/opt //arvr/projects/surreal/ar/slam/temple3/tools/python:simple_temple3 -- --vrs ${VRS_FILE} \
			--output-dir {OUTPUT_DIR} \

##-------------------------------------------------------------------------------
