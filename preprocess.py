import json
import os
import shutil
import sys
import time

import logging

logging.basicConfig(filename=f"logs/preprocess_{time.strftime('%Y%m%d')}.log", level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


# cmd = f"ffmpeg -i .\raw_videos\0001.mp4 -vf select='between(n\,1290\,1350)' -fps_mode vfr -q:v 2 .\frames\0001_%06d.jpeg"

def enable_hardware_acceleration():
    if os.popen('nvidia-smi').read():
        return "-hwaccel cuda "
    return ""


# def video_to_frames(video_path, output_dir, label, frame_start, frame_end):
#     if not os.path.exists(video_path):
#         logging.info(f"Video {video_path} does not exist")
#         return
#
#     video_id = os.path.basename(video_path).split('.')[0]
#     output_path = os.path.join(output_dir, video_id + '_' + label + '_%06d.jpeg')
#
#     logging.info(f'Extracting {video_path} {frame_start}:{frame_end} to {output_path}')
#
#     cmd = [
#         "ffmpeg",
#         # enable_hardware_acceleration(),
#         "-hide_banner -loglevel error",
#         f"-i {video_path}",
#         f"-vf \"select='between(n\\,{frame_start}\\,{frame_end})'\"",
#         "-fps_mode vfr",
#         "-q:v 2",
#         f"-start_number {frame_start}",
#         f"{output_path}",
#         "-r 2",
#     ]
#     cmd = " ".join(cmd)
#     os.system(cmd)


def video_to_frames(video_path, output_dir, label, frame_start, frame_end, step=5):
    for frame in range(frame_start, frame_end, step):
        video_id = os.path.basename(video_path).split('.')[0]
        output_path = os.path.join(output_dir, video_id + '_' + label + f'_{frame}.jpeg')

        logging.info(f'Extracting {video_path} {frame_start}:{frame_end} to {output_path}')

        cmd = [
            "ffmpeg",
            "-hide_banner -loglevel error",
            f"-i {video_path}",
            f"-vf \"select='eq(n\\,{frame})'\"",
            "-vframes 1",
            f"{output_path}",
        ]
        cmd = " ".join(cmd)
        os.system(cmd)


def videos_to_frames(index_file):
    content = json.load(open(index_file))

    for video in content:
        filename = video['video_id'] + '.mp4'
        video_path = os.path.join('raw_videos', filename)
        output_dir = 'frames'
        for plate in video['plates']:
            label = plate['label']
            video_to_frames(video_path, output_dir, label, plate['frame_start'], plate['frame_end'])


if __name__ == '__main__':
    if os.path.exists('frames'):
        shutil.rmtree('frames')
    os.mkdir('frames')

    input_file = 'icvlp_v0.1.json'
    videos_to_frames(input_file)
