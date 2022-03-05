import sys
from PIL import Image
from imutils import face_utils
import numpy as np
import dlib
import cv2
from threading import Thread
from queue import Queue
import os.path
import os
import logging
import argparse
import sys


SCALE_FACTOR = 0.2


# https://github.com/kairess/dog_face_detector/blob/master/video.py
def DetectFace(img_path, output_dir, dog_face_detector_dir):
    cnn_face_detection_model_v1_file = os.path.join(
        dog_face_detector_dir, 'dogHeadDetector.dat')
    if not os.path.exists(cnn_face_detection_model_v1_file):
        raise Exception(
            'dogHeadDetector.dat does not exist, please make sure this file is in --dog_face_detector_dir')
    detector = dlib.cnn_face_detection_model_v1(
        cnn_face_detection_model_v1_file)

    img_save_path = os.path.join(output_dir, os.path.basename(img_path))
    if os.path.exists(img_save_path):
        logging.info('skipping {}'.format(img_save_path))
        return

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, dsize=None, fx=SCALE_FACTOR, fy=SCALE_FACTOR)

    dets = detector(img, upsample_num_times=1)
    for i, d in enumerate(dets):
        logging.info('  ... detect %d: Left: %d Top: %d Right: %d Bottom: %d Confidence: %d' % (
            i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

        pil_img = Image.open(img_path)
        left, top, right, bottom = (
            int(d.rect.left() / SCALE_FACTOR), int(d.rect.top() / SCALE_FACTOR),
            int(d.rect.right() / SCALE_FACTOR), int(d.rect.bottom() / SCALE_FACTOR))

        img_res = pil_img.crop((left, top, right, bottom))
        img_res.save(img_save_path)
        logging.info('  ... wrote to %s' % img_save_path)

        return
    logging.info('NO %s' % img_path)


class Counter(object):
    def __init__(self):
        self.i = 0

    def Inc(self):
        res = self.i
        self.i += 1
        return res


class FaceDetectWorker(Thread):
    # https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

    def __init__(self, queue, c, n, output_dir, dog_face_detector_dir):
        Thread.__init__(self)
        self.queue = queue
        self.c = c
        self.n = n
        self.output_dir = output_dir
        self.dog_face_detector_dir = dog_face_detector_dir

    def run(self):
        while True:
            img_path = self.queue.get()
            n, d = self.c.Inc(), self.n
            logging.info('[%d / %d (%0.2f%%)] %s' % (n, d, 100*n/d, f))
            try:
                DetectFace(img_path, self.output_dir,
                           self.dog_face_detector_dir)
            except Exception as e:
                logging.error('error for %s: %s' % (f, e))
            finally:
                self.queue.task_done()


def MultiThreadedDetect(files, output_dir, dog_face_detector_dir):
    queue = Queue()
    c = Counter()
    for x in range(50):
        worker = FaceDetectWorker(queue, c, len(
            files), output_dir, dog_face_detector_dir)
        worker.start()
    # https://www.tutorialspoint.com/python/os_listdir.htm
    for f in files:
        queue.put(f)
    queue.join()


def SyncDetect(files, output_dir, dog_face_detector_dir):
    # https://www.tutorialspoint.com/python/os_listdir.htm
    for i, f in enumerate(files):
        logging.info('[{} / {}] {}'.format(i+1, len(files), f))
        n, d = i+1, len(files)
        logging.info('[%d / %d (%0.2f%%)] %s' % (n, d, 100*n/d, f))

        try:
            DetectFace(f, output_dir, dog_face_detector_dir)
        except Exception as e:
            logging.error('error for {}: {}'.format(f, e))


def Keep(f):
    _, ext = os.path.splitext(f)
    if ext != '.jpg' and ext != '.jpeg' and ext != '.png':
        return False
    if os.path.exists(f):
        return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=1)
    parser.add_argument('--multithreaded', '-m', action='store', type=bool)
    parser.add_argument('--input_dir', '-i', action='store',
                        type=str, required=True)
    parser.add_argument('--output_dir', '-o', action='store',
                        default='cropped', type=str)
    parser.add_argument('--dog_face_detector_dir', '-d',
                        default='../dog_face_detector', action='store', type=str)
    args, files = parser.parse_known_args()
    # https://gist.github.com/ms5/9f6df9c42a5f5435be0e
    args.verbose = 70 - (10*args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(level=args.verbose, format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    allfiles = [os.path.join(args.input_dir, f)
                for f in os.listdir(args.input_dir) if Keep(f)]
    allfiles.extend(files)
    for f in allfiles:
        if not os.path.exists(f):
            logging.error('{} does not exist, skipping'.format(f))
    allfiles = [f for f in allfiles if os.path.exists(f)]
    if args.multithreaded:
        MultiThreadedDetect(allfiles, args.output_dir,
                            args.dog_face_detector_dir)
    else:
        SyncDetect(allfiles, args.output_dir, args.dog_face_detector_dir)
