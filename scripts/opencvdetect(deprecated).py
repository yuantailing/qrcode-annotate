import cv2
import imageio
import json
import numpy as np
import os
import PIL.Image

root_dir = 'webimgs'

search_engines = ['360.en', '360.zh', 'baidu.en', 'baidu.zh', 'bing-cn.en', 'bing-cn.zh', 'bing-int.en', 'bing-int.zh', 'google.en', 'google.zh', 'sogou.en', 'sogou.zh', 'yahoo.en', 'yahoo.zh']

def compute_feature(img):
    assert len(img.shape) == 2 and img.shape[0] * img.shape[1] > 0
    feat1 = [img.shape[0], img.shape[1]]
    feat2 = cv2.resize(img, (5, 5), cv2.INTER_NEAREST) >= 128
    feat2 = feat2.reshape(-1).tolist()
    return tuple(feat1 + feat2)

results = dict()
qrCodeDetector = cv2.QRCodeDetector()

for search_engine in search_engines:
    folder = os.path.join(root_dir, search_engine)
    print(folder)
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        pil_img = PIL.Image.open(filepath)
        pil_img = pil_img.convert('RGB')
        img = np.array(pil_img, dtype=np.uint8)[:, :, ::-1]
        pts1 = qrCodeDetector.detectMulti(img)[1]
        if pts1 is None:
            pts1 = []
        else:
            pts1 = pts1.tolist()
        img = 255 - img
        pts2 = qrCodeDetector.detectMulti(img)[1]
        if pts2 is None:
            pts2 = []
        else:
            pts2 = pts2.tolist()
        if pts1 + pts2:
            print(len(pts1), '+', len(pts2))
        idname = f'{search_engine}/{os.path.splitext(filename)[0]}'
        results[idname] = pts1 + pts2

with open('cvdetectresult.json', 'w') as f:
    json.dump(results, f)
