cd ../..

###---------------assign recording------------------------------------------
# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria01'
# VRS_FILE_ID='recording_361553439261864'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria02'
# VRS_FILE_ID='recording_718712219224035'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria03'
# VRS_FILE_ID='recording_587699779415956'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/basketball/aria04'
# VRS_FILE_ID='recording_1185328285600927'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/dinner/aria01'
# VRS_FILE_ID='recording_581440823391395'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/dinner/aria02'
# VRS_FILE_ID='recording_366275142300476'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/dinner/aria03'
# VRS_FILE_ID='recording_534768578389716'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria01'
# VRS_FILE_ID='recording_1020978665123840'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria01'
# VRS_FILE_ID='recording_5382915405102602'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria01'
# VRS_FILE_ID='recording_618567999392322'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria01'
# VRS_FILE_ID='recording_676045747490248'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria02'
# VRS_FILE_ID='recording_589324752556502'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria02'
# VRS_FILE_ID='recording_722220612390942'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria03'
# VRS_FILE_ID='recording_3264381790516655'


# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/lego/aria03'
# VRS_FILE_ID='recording_5609571209077753'

###------------done till soccer----------------
# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria01'
# VRS_FILE_ID='recording_1094366114823255'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria01'
# VRS_FILE_ID='recording_1129067641009494'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria02'
# VRS_FILE_ID='recording_327130769634027'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria02'
# VRS_FILE_ID='recording_972600280086064'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria03'
# VRS_FILE_ID='recording_1199050950907098'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria03'
# VRS_FILE_ID='recording_2379118082242590'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria03'
# VRS_FILE_ID='recording_571516434369359'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria04'
# VRS_FILE_ID='recording_1088307072084972'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria04'
# VRS_FILE_ID='recording_404287518330316'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/soccer/aria04'
# VRS_FILE_ID='recording_446310274176531'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_1/aria02'
# VRS_FILE_ID='recording_444083367241805'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_1/aria04'
# VRS_FILE_ID='recording_1258004098341543'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_2/aria01'
# VRS_FILE_ID='recording_592094119166005'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_2/aria02'
# VRS_FILE_ID='recording_1090557211812566'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_2/aria03'
# VRS_FILE_ID='recording_731395581435977'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_2/aria04'
# VRS_FILE_ID='recording_1175684899882717'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_4/aria01'
# VRS_FILE_ID='recording_413309954192618'

# VRS_DIR='/home/rawalk/Desktop/datasets/ego_exo/raw/tagging_4/aria02'
# VRS_FILE_ID='recording_1116529889213265'

###---------------extract VRS------------------------------------------
mkdir -p $VRS_DIR/$VRS_FILE_ID
vrs extract-all $VRS_DIR/$VRS_FILE_ID.vrs --to $VRS_DIR/$VRS_FILE_ID


