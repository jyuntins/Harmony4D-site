import os
import sys

dir_path = sys.argv[1]

videos = [os.path.join(dir_path, name) for name in sorted(os.listdir(dir_path)) if name.endswith('.MP4')]


writelines = ["file '{}'\n".format(video) for video in videos]
f = open(os.path.join(dir_path, 'merge_list.txt'), "w")
f.writelines(writelines)
f.close()