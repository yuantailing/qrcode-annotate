import os
import numpy as np
import pyboof as pb


detector = pb.FactoryFiducial(np.uint8).qrcode()

root_nowrap = '../notwrapped'
root_wrap = '../wrapped'


for filename in os.listdir(root_wrap):
    image = pb.load_single_band(os.path.join(root_wrap, filename), np.uint8)
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
