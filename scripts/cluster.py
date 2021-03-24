import cv2
import imageio
import json
import os

from collections import defaultdict

root_dir = '../webimgs'

search_engines = ['360.en', '360.zh', 'baidu.en', 'baidu.zh', 'bing-cn.en', 'bing-cn.zh', 'bing-int.en', 'bing-int.zh', 'google.en', 'google.zh', 'sogou.en', 'sogou.zh', 'yahoo.en', 'yahoo.zh']

def compute_feature(img):
    assert len(img.shape) == 2 and img.shape[0] * img.shape[1] > 0
    feat1 = [img.shape[0], img.shape[1]]
    feat2 = cv2.resize(img, (5, 5), cv2.INTER_NEAREST) >= 128
    feat2 = feat2.reshape(-1).tolist()
    return tuple(feat1 + feat2)

clusters = defaultdict(list)

for search_engine in search_engines:
    folder = os.path.join(root_dir, search_engine)
    print(folder)
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        try:
            img = imageio.imread(filepath)
        except:
            print('load fail:', filepath)
            continue
        if len(img.shape) != 2:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        feat = compute_feature(img)
        clusters[feat].append(filepath)
        #print(filepath, feat)

with open('clusters.json', 'w') as f:
    json.dump(list(clusters.items()), f, indent=2)
