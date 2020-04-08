import os
import sys
import shutil
import cv2
import numpy as np


def get_paths(path_to_dir, extension='.mxf'):
    paths = []
    for file in os.listdir(path_to_dir):
        if file.endswith(extension):
            filename = file.replace(' ', '\\ ')
            paths.append(os.path.join(path_to_dir, filename))

    paths.sort()
    return paths


def mxf_to_mp4(src, dst):
    os.system("ffmpeg -loglevel panic -i %s -codec:v libx264 %s" % (src, dst))


def video_to_frames(src_path, dst_dir, fps=None, time=None):
    dst_dir = os.path.join(dst_dir, 'image-%5d.jpeg')
    if fps is not None:
        fps = ('-r %s' % (str(fps)))
    else:
        fps = ''
    if time is not None:
        time = ('-ss %s -t %s' % (str(time[0]), str(time[1])))
    else:
        time = ''
    os.system("ffmpeg -loglevel panic -i %s %s %s -qscale:v 2 %s" % (src_path, fps, time, dst_dir))


def frames_to_video(src_path, dst_path, fps=30):
    curr_dir = os.path.abspath(os.curdir)
    os.chdir(src_path)
    os.system("ffmpeg -loglevel panic -y -framerate %s -f image2 -i image-%%05d.jpeg %s" % (fps, dst_path))
    os.chdir(curr_dir)


def split_videos_into_frames(path_to_mp4, path_to_result, fps=30, time=None):
    '''
    time = (start_time, duration_time) in seconds
    '''
    print('Splitting *.mp4 to frames...')
    if not os.path.exists(path_to_result):
        os.makedirs(path_to_result)
    mp4_paths = get_paths(path_to_mp4, '.mp4')

    for src_path in mp4_paths:
        name = os.path.splitext(os.path.basename(src_path))[0]
        dst_dir = os.path.join(path_to_result, name)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        video_to_frames(src_path, dst_dir, fps=fps, time=time)
        frames_to_video(dst_dir, os.path.join("..", f"{name}.mp4"), fps=30)
        shutil.rmtree(dst_dir)

    print('Splitted videos:', len(mp4_paths))


def main():
    # path_to_mp4 = 'hp_chrkey_data/rotation_anton/'
    # path_to_norm_mp4 = 'hp_chrkey_data/rotation_anton/norm_30fps/'

    # path_to_mp4 = 'hp_chrkey_data/rotation_woman/'
    # path_to_norm_mp4 = 'hp_chrkey_data/rotation_woman/norm_30fps/'

    # path_to_mp4 = 'hp_chrkey_data/p4_fs_l50/'
    # path_to_norm_mp4 = 'hp_chrkey_data/p4_fs_l50/norm_30fps/'

    # path_to_mp4 = 'hp_chrkey_data/p4_fs_l100/'
    # path_to_norm_mp4 = 'hp_chrkey_data/p4_fs_l100/norm_30fps/'

    path_to_mp4 = sys.argv[1]
    path_to_norm_mp4 = os.path.join(path_to_mp4, "norm_30fps")

    split_videos_into_frames(path_to_mp4, path_to_norm_mp4, fps=30, time=(1, 10))


if __name__ == "__main__":
    main()
