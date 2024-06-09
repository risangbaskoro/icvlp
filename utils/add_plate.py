#!/usr/bin/env python

import json
import logging
import os.path


def get_plate_instances(target_plate):
    target_plate = target_plate.upper()

    content = json.load(open(os.path.join(os.getcwd(), 'icvlp_v0.1.json')))

    instances = []

    for video in content:
        for plate in video['plates']:
            label = plate['label']
            if target_plate == label.upper():
                instances.append(plate)

    return instances


def check_plate():
    plate = input('Check Number Plate: ').upper()
    plates = get_plate_instances(plate)

    print(json.dumps(plates, indent=2))
    print("\nNumber of instances:", len(plates))


def add_plate(content, target_video_id, new_label, new_frame_start, new_frame_end):
    video = next((video for video in content if video['video_id'] == target_video_id), None)
    plates = video['plates']
    new_plate = {
        'label': new_label,
        'frame_start': new_frame_start,
        'frame_end': new_frame_end,
        'frames': []
    }
    plates.append(new_plate)
    video['plates'] = plates
    return json.loads(json.dumps(new_plate))


def add_plate_to_video(id):
    input_file = os.path.join(os.getcwd(), 'icvlp_v0.1.json')
    content = json.load(open(input_file))

    index = next((index for index, video in enumerate(content) if video['video_id'] == video_id), None)

    if index is None:
        logging.error('video_id not found')
        return

    label = input('Enter label: ').upper()

    if len(label) < 6 or len(label) > 9:
        logging.error('Label length must be between 6 and 9')
        return

    frame_start = int(input('Enter frame_start: '))
    frame_end = int(input('Enter frame_end: '))

    if frame_start > frame_end:
        logging.error('Frame start must be less than frame end')
        return

    adds = add_plate(content, video_id, label, frame_start, frame_end)
    assert content[index]['plates'][-1] == adds

    print()
    print(json.dumps(adds, indent=2))
    print()

    json.dump(content, open(input_file, 'w'), indent=2)


if __name__ == '__main__':
    repeat = True
    os.system('cls' if os.name == 'nt' else 'clear')

    check_exists = input('Do you want to check if the plate exists first? (y/N): ').lower() == 'y'

    video_id = None

    while repeat:
        if not video_id and not check_exists:
            video_id = int(input('Enter video_id: '))

            if isinstance(video_id, int):
                video_id = str(video_id).zfill(4)

        os.system('cls' if os.name == 'nt' else 'clear')
        if check_exists:
            check_plate()
            check_exists = False
        else:
            print(f"video_id {video_id} ({video_id}.mp4) \n")
            add_plate_to_video(video_id)

        again = input('Continue? (ENTER/c/q) ')

        check_exists = again.lower() == 'c'
        repeat = again.lower() != 'q'
