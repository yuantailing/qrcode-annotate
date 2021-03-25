import os
import numpy as np
import pyboof as pb
import sys

detector = pb.FactoryFiducial(np.uint8).qrcode()

img_dir = sys.argv[1]

for filename in os.listdir(img_dir):
    image = pb.load_single_band(os.path.join(img_dir, filename), np.uint8)
    detector.detect(image)
    for detection in detector.detections:
        print(filename, 'success', detection.verson, detection.error_level, end=' ')
        for x in detection.rawbits:
            s = bin(x)[2:]
            s = '0' * (8 - len(s)) + s
            print(s, end='')
        print()
    for detection in detector.failures:
        if not detection.rawbits:
            continue
        print(filename, 'failure', detection.verson, detection.error_level, end=' ')
        for x in detection.rawbits:
            s = bin(x)[2:]
            s = '0' * (8 - len(s)) + s
            print(s, end='')
        print()
