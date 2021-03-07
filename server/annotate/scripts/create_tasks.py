import json
import os

from annotate.models import *
from django.db import transaction

@transaction.atomic
def run(*args):
    with open(os.path.join(webimgs_root_dir, '../same.json')) as f:
        same = json.load(f)
    ignored = set()
    for a, b in same:
        search_engine, image_id = b.split('/')[-2:]
        image_id = os.path.splitext(image_id)[0]
        idname = f'{search_engine}/{image_id}'
        ignored.add(idname)

    for folder in sorted(os.listdir(webimgs_root_dir)):
        for filename in sorted(os.listdir(os.path.join(webimgs_root_dir, folder))):
            filepath = os.path.join(webimgs_root_dir, folder, filename)
            idname, ext = os.path.splitext('/'.join([folder, filename]))
            if idname not in ignored:
                Task.objects.create(idname=idname, finished=0, prop_photo=0, prop_occluded=0, prop_art=0, prop_st=0)
        print(folder)
