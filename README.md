![Banner Image](https://data.risangbaskoro.com/cvlpr/banner.png)

<h2 align="center">
    Indonesian Commercial Vehicle License Plate (ICVLP)
    Dataset
</h2>

> [!WARNING]
> Work in progress.

The data is in json file. The `download_video.py` and `preprocess.py` scripts are included to download and preprocess
the dataset.

## Data Description

The json file is an array of objects with the following description:

### `Video`

| name     | datatype     | description                                        |
|----------|--------------|----------------------------------------------------|
| video_id | str          | unique video identifier                            |
| source   | str          | string identifier for the source site (or channel) |
| url      | str          | url where the video will be downloaded from        |
| fps      | str          | video frame rate when preprocessing                |
| plates   | array<Plate> | array of `Plate` that is in the video frames       |

### `Plate`

| name        | datatype     | description                                          |
|-------------|--------------|------------------------------------------------------|
| label       | str          | the license plate number                             |
| frame_start | int          | frame where the plate is first appeared in the video |
| frame_end   | int          | frame where the plate is last appeared in the video  |
| frames      | array<Frame> | WIP                                                  |

### `Frame`

| name | datatype | description |
|------|----------|-------------|
|      |          |             |
