## commands to start docker and start the x forwarding
# sudo systemctl start docker
## xhost +local:docker
##// run the colmap docker

xhost +local:docker
bash ~/Desktop/ego/colmap/scripts/_run/run_docker.sh

## then at the terminal
## colmap gui

## File -> New project

## Database -> $WORKPLACE/temp.db
## Images -> $OUTPUTDIR/images

## Fature extraction
## Camera model -> OPENCV,
## Note the OPENCV_FULL_MODEL does not converge well.
## check on the shared per sub folder

## Feature matching
## Run


