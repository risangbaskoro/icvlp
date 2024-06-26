#!/usr/bin/env python
import json
import os
import sys
import time

import cv2

from tqdm import tqdm, trange

import logging

logging.basicConfig(filename=f"logs/extract_frames_{time.strftime('%Y%m%d')}.log", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def video_to_frames(video_path, output_dir, label, frame_start, frame_end, fps=25):
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    step = int(video_fps // fps)

    frames_extracted = 0
    for frame_number in trange(frame_start, frame_end + 1, step,
                               desc=label, position=1, leave=False):
        video_id = os.path.basename(video_path).split('.')[0]
        output_path = os.path.join(output_dir, f"{video_id}_{frame_number}_{label}.jpeg")
        if os.path.exists(output_path):
            logging.debug(f'Skipping {output_path}: image already exists')
            continue

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        ret, frame = cap.read()

        logging.debug(f'Processing {video_path} {frame_start}:{frame_end} to {output_path}')
        try:
            cv2.imwrite(output_path, frame)
            frames_extracted += 1
        except Exception as e:
            logging.error(f'Cannot write to {output_path}: {e}')

    cap.release()
    return frames_extracted


def videos_to_frames(index_file):
    content = json.load(open(index_file))

    videos_processed = 0
    frames_extracted = 0
    plate_extracted = 0
    for video in content:
        filename = video['video_id'] + '.mp4'
        video_path = os.path.join('raw_videos', filename)

        if not os.path.exists(video_path):
            logging.info(f'Skipping {video_path}: video does not exist')
            continue

        output_dir = 'frames'
        plates = video['plates']
        fps = video['fps']

        if len(plates) == 0:
            continue

        videos_processed += 1
        for plate in tqdm(plates, desc=f"{video_path}", position=0, leave=False):
            label = plate['label']
            frame_start, frame_end = plate['frame_start'], plate['frame_end']

            if frame_start > frame_end:
                logging.error(f"Frame start is larger than frame end in video_id:{filename} and label:{label}")
                continue

            frames_extracted += video_to_frames(video_path, output_dir, label, frame_start, frame_end, fps=fps)
            plate_extracted += 1

    logging.info(
        f"{frames_extracted} frames extracted ({plate_extracted} plates processed) from {videos_processed} videos"
    )


if __name__ == '__main__':
    if not os.path.exists("frames"):
        os.mkdir("frames")

    since = time.time()
    input_file = 'icvlp_v0.1.json'
    videos_to_frames(input_file)
    logging.info(f'Finished processing {input_file} in {time.time() - since:.2f} seconds')
