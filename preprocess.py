#!/usr/bin/env python
import glob
import json
import os
import sys
import time

import cv2

from tqdm import tqdm, trange

import logging

logging.basicConfig(filename=f"logs/extract_frames_{time.strftime('%Y%m%d')}.log", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def extract_frame(video_path, output_dir, plate, instance_num):
    cap = cv2.VideoCapture(video_path)
    label = plate['label']

    plates_extracted = 0
    for frame in plate['frames']:
        output_name = f"{label}_{instance_num + 1}.jpeg"
        output_path = os.path.join(output_dir, output_name)
        frame_number = frame['frame']
        bbox = frame['bbox']
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, image = cap.read()

        # y_min:y_max, x_min:x_max
        img = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        cv2.imwrite(output_path, img)
        plates_extracted += 1
        instance_num += 1

    cap.release()
    return plates_extracted


def extract_frames(index_file, output_dir):
    content = json.load(open(index_file))

    for video in content:
        filename = video['video_id'] + '.mp4'
        video_path = os.path.join('raw_videos', filename)

        if not os.path.exists(video_path):
            logging.info(f'Skipping {video_path}: video does not exist')
            continue

        plates = video['plates']
        for plate in plates:
            if not len(plate['frames']):
                continue
            existing_plate_files = [int(num.split('_')[-1].split('.')[0]) for num in
                                    glob.glob(os.path.join(output_dir, plate['label'] + '*.jpeg'))]
            instance_num = sorted(existing_plate_files, reverse=True)[0] if existing_plate_files else 0
            extract_frame(video_path, output_dir, plate, instance_num)


if __name__ == '__main__':
    INDEX_FILE = 'icvlp_v0.1.json'
    TARGET_DIR = 'images'

    if not os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)

    extract_frames(INDEX_FILE, TARGET_DIR)
