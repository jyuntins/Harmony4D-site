# ###-----------------restructure your folder as follows------------------------------
# - BIG_SEQUENCE
# 	- aria01
# 		- recording
# 			- paste the trajectory folder - rename as trajectory_info
# 			- trajectory.csv (full_trajectory.csv from the trajectory_info folder. Copied and renamed.)
# 			- rename the vrs file as video.vrs
# 		- gt-metadata.json (create one if not present)


###----------------------------------------------------------------------------
# BIG_SEQUENCE='basketball'
# BIG_SEQUENCE='frisbee_1'
# BIG_SEQUENCE='frisbee_2'
# BIG_SEQUENCE='tagging_1'
# BIG_SEQUENCE='lego_assemble'
# BIG_SEQUENCE='lego_disassemble'
# BIG_SEQUENCE='tagging_2'
# BIG_SEQUENCE='tagging_3'
# BIG_SEQUENCE='soccer_1'
# BIG_SEQUENCE='soccer_2'
# BIG_SEQUENCE='soccer_3'
# BIG_SEQUENCE='soccer_4'
# BIG_SEQUENCE='soccer_5'
BIG_SEQUENCE='pro_soccer'


DATA_DIR="/home/rawalk/Desktop/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"

# RECORDING=aria01
# RECORDING=aria02
# RECORDING=aria03
RECORDING=aria04
# RECORDING=aria05
# RECORDING=aria06

###----------------------------------------------------------------------------
### if fbsource is empty, run "eden restart". And then cd back
## make sure you have the gt-metadata.json file.
## it looks like

# {	
# 	"aria": 
# 		{"subtour_name": "recording", "device_serial": "recording", "device_dlr_name": "Aria_MCM", 
# 		"device_dlr_id": "422298619330741", "dt_Optitrack_Ariaimu_ns": 171338973000000.0}
# }

####-----------------------------------------------------------------------------
cd ~/fbsource/arvr/projects/surreal/experiments/PseudoGT/experiments
buck run @arvr/mode/linux/cuda11/opt //arvr/projects/surreal/experiments/PseudoGT/experiments:pseudo_gt -- --folder ${DATA_DIR} --name ${RECORDING}