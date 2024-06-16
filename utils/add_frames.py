import glob
import json
import os

import xml.etree.ElementTree as et


def get_bounding_boxes(xml_path):
    if not os.path.exists(xml_path):
        return
    tree = et.parse(xml_path)
    root = tree.getroot()

    filename = root.find('filename').text.split('.')[0]

    video_id, frame, label = filename.split('_')

    obj = root.find('object')

    if obj is None:
        return

    bbox = obj.find('bndbox')
    bbox = [
        round(float(bbox.find('xmin').text)),
        round(float(bbox.find('ymin').text)),
        round(float(bbox.find('xmax').text)),
        round(float(bbox.find('ymax').text))
    ]

    return {
        'frame': int(frame),
        'bbox': bbox
    }


def get_xml_files(plate_data):
    label = plate_data['label']
    pattern = os.path.join('frames', f'*_{label}.*')
    filenames = glob.glob(pattern)
    tmp = []
    for filename in filenames:
        video_id, frame, label = os.path.basename(filename).split('.')[0].split('_')
        tmp.append((video_id, int(frame), label))
    tmp = sorted(tmp)
    filenames = ['_'.join([video_id, str(frame), label + '.xml']) for video_id, frame, label in tmp]
    return filenames


if __name__ == '__main__':
    INDEX_FILE = os.path.join(os.getcwd(), 'icvlp_v0.1.json')
    content = json.load(open(INDEX_FILE))

    for video in content:
        for plate in video['plates']:
            paths = get_xml_files(plate)
            plate['frames'] = []
            for path in paths:
                path = os.path.join('annotations', path)
                box = get_bounding_boxes(path)
                if box is None:
                    continue
                plate['frames'].append(box)

    json.dump(content, open(INDEX_FILE, 'w'), indent=2)
