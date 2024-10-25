cd ../..

# VRS_FILE='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria01/recording_361553439261864.vrs'
# OUTPUT_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria01/recording_361553439261864'

# VRS_FILE='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria02/recording_718712219224035.vrs'
# OUTPUT_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria02/recording_718712219224035'

# VRS_FILE='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria03/recording_587699779415956.vrs'
# OUTPUT_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria03/recording_587699779415956'


###------------------------lego--------------------------------------
VRS_FILE='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria01/recording_618567999392322.vrs'
OUTPUT_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria01/recording_618567999392322'

###----------------------------------------------------------------------------------------------
OUTPUT_DIR=${OUTPUT_DIR}_temple2 ## main folder for output dump
OUTPUT_MAP_FILE=${OUTPUT_DIR}/map.db

rm -rf ${OUTPUT_DIR}
mkdir -p ${OUTPUT_DIR}

###----------------------------------------------------------------------------------------------
##----cd to fbsource----
cd ~/fbsource
buck run @arvr/mode/linux/opt temple2 -- --slam-settings arvr/projects/surreal/data/SparseSettings/settings_Temple2_default.json \
			-o ${OUTPUT_DIR} \
			--map-dest ${OUTPUT_MAP_FILE} \
			--db-type local \
			--voc arvr/projects/surreal/ar/data/vocabulary/voc_FREAK32_6levels_10branch_70radius_thrift.bin \
			--override temple2_highfrequencylogger_enable=true \
			--autoplay vrs ${VRS_FILE}

##-------------------------------------------------------------------------------


########-------------------run on OD GPU, this is the main command!-----------------------
## can only use the sample_ids.yaml
## make it look like
# input_vrs:
#     - manifold://spaceport_data/tree/rawalProject/basketball/aria01/recording_361553439261864.vrs
#     - manifold://spaceport_data/tree/rawalProject/basketball/aria02/recording_718712219224035.vrs
#     - manifold://spaceport_data/tree/rawalProject/basketball/aria03/recording_587699779415956.vrs
#     - manifold://spaceport_data/tree/rawalProject/basketball/aria04/recording_1185328285600927.vrs


###-----------for all trajectories---------------------------
### 48 trajectories, 52 - 4.
# input_vrs:
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1011430629549683.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1020978665123840.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1088307072084972.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1090557211812566.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1094366114823255.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1116529889213265.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1120979198454847.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1129067641009494.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1175684899882717.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1199050950907098.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1249537799211084.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1258004098341543.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1656706208047102.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1734630476901520.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1954516401605238.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_2379118082242590.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_3172966819683702.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_3264381790516655.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_327130769634027.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_364003889085826.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_366275142300476.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_404287518330316.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_413309954192618.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_426067416216805.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_444083367241805.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_446310274176531.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_466078801723481.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_469364431330744.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_5273127309435193.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_534768578389716.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_5382915405102602.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_5609571209077753.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_571516434369359.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_581440823391395.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_589324752556502.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_592094119166005.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_618567999392322.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_676045747490248.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_722220612390942.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_731395581435977.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_733815391031759.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_753848652701712.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_757897562191728.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_764245114818138.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_790039588794009.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_804928087337433.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_865269541113723.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_972600280086064.vrs


###-----------only soccer and frisbee---------------------------
# input_vrs:
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1734630476901520.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1954516401605238.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_865269541113723.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_5273127309435193.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_466078801723481.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_804928087337433.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1120979198454847.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1249537799211084.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1656706208047102.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_757897562191728.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_790039588794009.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_426067416216805.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_1011430629549683.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_733815391031759.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_764245114818138.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_469364431330744.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_753848652701712.vrs
	# - manifold://spaceport_data/tree/rawalProject/all/recording_3172966819683702.vrs

# or use the gaia versions
# input_vrs:
#     - gaia:1734630476901520
#     - gaia:1954516401605238
#     - gaia:865269541113723
#     - gaia:5273127309435193
#     - gaia:466078801723481
#     - gaia:804928087337433
#     - gaia:1120979198454847
#     - gaia:1249537799211084
#     - gaia:1656706208047102
#     - gaia:757897562191728
#     - gaia:790039588794009
#     - gaia:426067416216805
#     - gaia:1011430629549683
#     - gaia:733815391031759
#     - gaia:764245114818138
#     - gaia:469364431330744
#     - gaia:753848652701712
#     - gaia:3172966819683702

# ###---------only tagging1 and tagging2-----------------------
# input_vrs:
#     - gaia:592094119166005
#     - gaia:1258004098341543
#     - gaia:1175684899882717
#     - gaia:731395581435977
#     - gaia:444083367241805
#     - gaia:1090557211812566
    
# ###---------only lego and dinner-----------------------
# input_vrs:
#     - gaia:1020978665123840
#     - gaia:676045747490248
#     - gaia:5382915405102602
#     - gaia:618567999392322
#     - gaia:581440823391395
#     - gaia:5609571209077753
#     - gaia:3264381790516655
#     - gaia:534768578389716
#     - gaia:589324752556502
#     - gaia:722220612390942
#     - gaia:366275142300476
#     - gaia:364003889085826

# ###---------only old_soccer-----------------------
# input_vrs:
#     - gaia:1094366114823255
#     - gaia:1129067641009494
#     - gaia:413309954192618
#     - gaia:446310274176531
#     - gaia:404287518330316
#     - gaia:1088307072084972
#     - gaia:571516434369359
#     - gaia:1199050950907098
#     - gaia:2379118082242590
#     - gaia:972600280086064
#     - gaia:327130769634027
#     - gaia:1116529889213265

# ### tagging_3
# input_vrs:
#     - gaia:413309954192618
#     - gaia:1116529889213265

# ### pro_soccer
# input_vrs:
#     - gaia:865269541113723
#     - gaia:804928087337433
#     - gaia:1656706208047102
#     - gaia:426067416216805
#     - gaia:764245114818138
#     - gaia:469364431330744

# ### pro_soccer_part2
# input_vrs:
#     - gaia:469364431330744
#     - gaia:764245114818138
#     - gaia:426067416216805

## then run 
# cd ~/fbcode/surreal/spaceport
# buck2 build @mode/opt -c python.package_style=inplace --show-output //surreal/spaceport:batch_label_direct
# $HOME/fbsource/buck-out/v2/gen/fbcode/d5479947763d4841/surreal/spaceport/__batch_label_direct__/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /tmp/soccer_frisbee --trajectory_only

#now open the folder /tmp/rawal in VScode and download


####------------new working command--------------------------
### make sure the tab space is identical in the config/sample_ids.yaml file
# cd ~/fbcode/surreal/spaceport
# buck2 build @mode/opt -c python.package_style=inplace --show-output //surreal/spaceport:batch_label_direct 
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /tmp/soccer_frisbee --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /tmp/all --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /tmp/tagging1_2 --trajectory_only

# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /tmp/lego_dinner --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /tmp/old_soccer --trajectory_only

# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/dinner --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/frisbee_1 --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/frisbee_2 --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/lego --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/soccer_1 --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/soccer_1v1 --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/tagging_1 --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/tagging_2 --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/tagging_3 --trajectory_only
# $HOME/fbsource/buck-out/v2/gen/fbcode/surreal/spaceport/batch_label_direct.par  --input_yaml config/sample_ids.yaml --spaceport_root /home/rawalk/trajectory/pro_soccer_part2 --trajectory_only