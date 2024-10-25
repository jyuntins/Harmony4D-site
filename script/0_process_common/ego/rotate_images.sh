# DIR='/home/rawalk/Desktop/datasets/ego_exo/images/008_basketball_1/aria03/'
# DIR='/home/rawalk/Desktop/datasets/ego_exo/current_dev/basketball/ego/aria01/rotated_images/'
# DIR='/home/rawalk/Desktop/datasets/ego_exo/current_dev/basketball/ego/aria02/rotated_images/'
# DIR='/home/rawalk/Desktop/datasets/ego_exo/current_dev/basketball/ego/aria03/rotated_images/'
# DIR='/home/rawalk/Desktop/datasets/ego_exo/current_dev/basketball/ego/aria04/rotated_images/'

DIR=$1

for szFile in $DIR/*.jpg
do 
    convert "$szFile" -rotate 90 $DIR/"$(basename "$szFile")" ; 
done
