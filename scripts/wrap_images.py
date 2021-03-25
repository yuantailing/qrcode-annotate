import cv2
import json
import os
import numpy as np
import PIL.Image

webimgs_root = '../webimgs'
dst_root = 'wrapped-mirror'
nowrap_root = 'notwrapped-mirror'

def regular_box(points, idname):
    if len(points) == 2:
        points = [points[0], [points[0][0], points[1][1]], points[1], [points[1][0], points[0][1]]]
    elif len(points) == 3:
        points = [points[0], points[1], points[2], [points[0][0] - points[1][0] + points[2][0], points[0][1] - points[1][1] + points[2][1]]]
    elif len(points) == 4:
        pass
    else:
        raise NotImplementedError
    line1 = (points[1][0] - points[0][0], points[1][1] - points[0][1])
    line2 = (points[2][0] - points[1][0], points[2][1] - points[1][1])
    if line1[0] * line2[1] - line1[1] * line2[0] < 0:
        points = [points[0], points[3], points[2], points[1]]
    while points[0][0] + points[0][1] > min(p[0] + p[1] for p in points):
        points = [points[1], points[2], points[3], points[0]]
    return points

with open('boxes.json') as f:
    all_boxes = json.load(f)
for idname in all_boxes.keys():
    all_boxes[idname] = [regular_box(box, idname) for box in all_boxes[idname]['boxes'] if len(box) >= 2 and all(p[0] is not None and p[1] is not None for p in box)]
all_boxes = {k: v for k, v in all_boxes.items() if len(v) >= 1}

# 相同图片
with open('same.json') as f:
    same_pairs = json.load(f)
same_map = dict()
for a, b in same_pairs:
    search_engine, image_id = a.split('/')[-2:]
    image_id = os.path.splitext(image_id)[0]
    a = f'{search_engine}/{image_id}'
    search_engine, image_id = b.split('/')[-2:]
    image_id = os.path.splitext(image_id)[0]
    b = f'{search_engine}/{image_id}'
    same_map[b] = a

# 检查 ZXing 直接能解码的图片都有标注
more_decoded = set()
with open('zxing_direct_decode.txt') as f:
    for line in f:
        search_engine, image_id, result = line.split()
        if result.startswith('com.google.zxing'):
            continue
        idname = f'{search_engine}/{image_id}'
        while idname in same_map:
            idname = same_map[idname]
        assert idname in all_boxes

print(len(all_boxes))

# ===============
# ===============
# ===============
def get_filepath(idname):
    exts = ['.png', '.jpeg', '.gif']
    for ext in exts:
        filepath = os.path.join(webimgs_root, idname + ext)
        if os.path.isfile(filepath):
            return filepath
    raise ValueError

def load_cv_image(idname):
    filepath = get_filepath(idname)
    pil_img = PIL.Image.open(filepath)
    pil_img = pil_img.convert('RGBA')
    background = PIL.Image.new('RGB', size=pil_img.size, color=(255,255,255))
    background.paste(pil_img, mask=pil_img)
    img = np.array(background, dtype=np.uint8)[:, :, ::-1].copy()
    return img

if not os.path.isdir(dst_root):
    os.makedirs(dst_root)
if not os.path.isdir(nowrap_root):
    os.makedirs(nowrap_root)

for idname, boxes in sorted(all_boxes.items()):
    img = load_cv_image(idname)
    for i, box in enumerate(boxes):
        border = 50
        length = 300
        pts2 = np.float32([[border, border], [border + length, border], [border + length, border + length], [border, border + length]])
        pts1 = np.float32(box)
        M = cv2.getPerspectiveTransform(pts1, pts2)
        wrapped = cv2.warpPerspective(img, M, (2 * border + length, 2 * border + length), borderValue=[255, 255, 255])
        cv2.imwrite(os.path.join(dst_root, idname.replace('/', '+') + f'-{i}-o-0.png'), wrapped[:,::-1], [cv2.IMWRITE_PNG_COMPRESSION, 3])
        cv2.imwrite(os.path.join(dst_root, idname.replace('/', '+') + f'-{i}-r-0.png'), (255 - wrapped)[:,::-1], [cv2.IMWRITE_PNG_COMPRESSION, 3])

for search_engine in os.listdir(webimgs_root):
    src_dir = os.path.join(webimgs_root, search_engine)
    for filename in os.listdir(src_dir):
        id = int(os.path.splitext(filename)[0])
        idname = f'{search_engine}/{id}'
        img = load_cv_image(idname)
        cv2.imwrite(os.path.join(nowrap_root, idname.replace('/', '+') + '-orig.png'), img[:,::-1], [cv2.IMWRITE_PNG_COMPRESSION, 3])
        cv2.imwrite(os.path.join(nowrap_root, idname.replace('/', '+') + '-reverse.png'), (255 - img)[:,::-1], [cv2.IMWRITE_PNG_COMPRESSION, 3])
