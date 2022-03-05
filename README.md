# dogfacedetect

This will crop images around dog faces. e.g.

| Source Image                                                         | Cropped Image                                                         |
| -------------------------------------------------------------------- | --------------------------------------------------------------------- |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/1.jpg) | ![output 1](https://spudtrooper.github.io/dogfacedetect/output/1.jpg) |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/2.jpg) | ![output 2](https://spudtrooper.github.io/dogfacedetect/output/2.jpg) |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/3.jpg) | ![output 3](https://spudtrooper.github.io/dogfacedetect/output/3.jpg) |
| ![intput 1](https://spudtrooper.github.io/dogfacedetect/input/4.jpg) | ![output 4](https://spudtrooper.github.io/dogfacedetect/output/4.png) |

## Usage

Clone [https://github.com/kairess/dog_face_detector](https://github.com/kairess/dog_face_detector) 
and set the `--dog_face_detector_dir` to the directory to which it's cloned. e.g.

```
cd /Users/bob/projects
git clone https://github.com/kairess/dog_face_detector
```

Run with `scripts/run.sh` specifying the files to crop with:

* the flag `--input_dir` - crop all image files under this directory
* arguments - crop all the images after the flags

e.g. for directory `image-files` and two images `one.jpg`, `two.jpeg`.

```
$ scripts/run.sh --dog_face_detector_dir /Users/bob/projects/dog_face_detector --input_dir image-files one.jpg two.jpeg
```

## For Jeff

Fix the python path before running

```
export PYTHONPATH=/opt/homebrew/lib/python3.9/site-packages
```