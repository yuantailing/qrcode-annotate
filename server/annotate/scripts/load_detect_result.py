import json
import os

from annotate.models import *
from django.db import transaction

@transaction.atomic
def run(*args):
    with open(os.path.join(webimgs_root_dir, '../detectresult.json')) as f:
        results = json.load(f)
    for idname, points in results.items():
        Task.objects.filter(id__gt=7000, idname=idname).update(boxes=json.dumps([points]))
