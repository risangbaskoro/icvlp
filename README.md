![Banner Image](https://data.risangbaskoro.com/cvlpr/banner.png)

<h2 align="center">
    Indonesian Commercial Vehicle License Plate (ICVLP)
    Dataset
</h2>

> [!WARNING]
> Work in progress.

## Data Description

| name     | datatype | description                                                                                   |
|----------|----------|-----------------------------------------------------------------------------------------------|
| label    | `str`    | labels of the license plate                                                                   |
| video_id | `str`    | unique video identifier                                                                       |
| source   | `str`    | string identifier for the source site                                                         |
| url      | `str`    | url where the video will be downloaded                                                        |
| fps      | `int`    | video frame rate                                                                              |
| split    | `str`    | subset which the sample belongs                                                               |
| bboxes   | `[int]`  | bounding box of the license plate. Following OpenCV convention, (0, 0) is the up-left corner. |
