#!/usr/bin/env python

import json
import os
import random
import sys
import time

import logging

logging.basicConfig(filename=f"logs/download_{time.strftime('%Y%m%d')}.log", level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

YOUTUBE_DOWNLOADER = "yt-dlp"


def check_youtube_dl_version():
    version = os.popen(f'{YOUTUBE_DOWNLOADER} --version').read()
    assert version, f"{YOUTUBE_DOWNLOADER} cannot be found in PATH. Please verify your installation."


def download_youtube_video(video_url, saveto, video_id):
    cmd = [
        YOUTUBE_DOWNLOADER,
        video_url,
        f"-o {os.path.join(saveto, video_id + '.mp4')}",
        f"--format mp4",
        "-f 'bestvideo[height<=1080][ext=mp4]+best'"
    ]
    cmd = ' '.join(cmd)

    rv = os.system(cmd)

    if not rv:
        logging.info(f'Finish downloading YouTube video url {video_url}')
    else:
        logging.error(f'Unsuccessful downloading YouTube video url {video_url}')


def download_youtube_videos(index_file, saveto='raw_videos'):
    content = json.load(open(index_file))

    if not os.path.exists(saveto):
        os.mkdir(saveto)

    for entry in content:
        video_id = entry['video_id']
        video_url = entry['url']

        if 'youtube' not in video_url and 'youtu.be' not in video_url:
            continue

        if os.path.exists(os.path.join(saveto, video_id + 'mp4')):
            logging.info(f'YouTube video {video_id} is already exists.')
            continue
        else:
            download_youtube_video(video_url, saveto, video_id)

            # Reduce the download frequency, avoid spam
            time.sleep(random.uniform(1.0, 1.5))


if __name__ == '__main__':
    index = 'icvlp_v0.1.json'

    logging.info('Start downloading YouTube videos.')
    logging.info(f'Index file: {index}')
    check_youtube_dl_version()
    download_youtube_videos(index)
