import json
import logging
import os.path
import sys


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


def main():
    input_file = os.path.join(os.getcwd(), 'icvlp_v0.1.json')
    content = json.load(open(input_file))

    video_id = int(input('Enter video_id: '))

    if isinstance(video_id, int):
        video_id = str(video_id).zfill(4)

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

    print(json.dumps(adds, indent=2))

    json.dump(content, open(input_file, 'w'), indent=2)


if __name__ == '__main__':
    repeat = True
    while repeat:
        main()
        again = input('Continue?')
        repeat = again == ''
