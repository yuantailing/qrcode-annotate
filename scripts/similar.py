import cv2
import imageio
import json
import math
import numpy
import os
import shutil


def compute_psnr(img1, img2):
    mse = numpy.mean((img1 - img2) ** 2)
    if mse == 0:
        return 10000
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

with open('clusters.json') as f:
    clusters = json.load(f)


same = []
for cluster_id, (feat, filepaths) in enumerate(clusters):
    if len(filepaths) <= 1:
        continue
    imgs = []
    for filepath in filepaths:
        img = imageio.imread(filepath)
        if len(img.shape) != 2:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        imgs.append(img)
    for i in range(len(imgs)):
        for j in range(i + 1, len(imgs)):
            psnr = compute_psnr(imgs[i], imgs[j])
            if psnr == 10000:
                same.append([filepaths[i].replace('\\', '/'), filepaths[j].replace('\\', '/')])

with open('same.json', 'w') as f:
    json.dump(same, f)
