# dogfacedetect

This will crop images around dog faces. e.g.

| Source Image                                                         | Cropped Image                                                         |
| -------------------------------------------------------------------- | --------------------------------------------------------------------- |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/1.jpg) | ![output 1](https://spudtrooper.github.io/dogfacedetect/output/1.jpg) |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/2.jpg) | ![output 2](https://spudtrooper.github.io/dogfacedetect/output/2.jpg) |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/3.jpg) | ![output 3](https://spudtrooper.github.io/dogfacedetect/output/3.jpg) |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/4.png) | ![output 4](https://spudtrooper.github.io/dogfacedetect/output/4.png) |

Initially used to create the source images for https://spudtrooper.github.io/photocollage-java/stella-head-200w25xh25-out.png.

## Usage

Run with `scripts/run.sh` specifying the files to crop with:

* the flag `--input_dir` - crop all image files under this directory
* arguments - crop all the images after the flags

e.g. for directory `image-files` and two images `one.jpg`, `two.jpeg`.

```
$ scripts/run.sh --dog_face_detector_dir /Users/bob/projects/dog_face_detector --input_dir image-files one.jpg two.jpeg
```

## Thanks

The model comes from https://github.com/kairess/dog_face_detector.

## For Jeff

Fix the python path before running (probably figure how to do this correctly)

```
export PYTHONPATH=/opt/homebrew/lib/python3.9/site-packages
```