import random

from annotate.models import *
from django.db import transaction

@transaction.atomic
def run(*args):
    tasks = list(Task.objects.filter(id__gt=6760))
    for i in range(len(tasks)):
        j = random.randrange(i, len(tasks))
        if i == j:
            continue
        print('swap', tasks[i].id, tasks[j].id)
        name2 = tasks[j].idname
        tasks[j].idname = 'tmp'
        tasks[j].save()
        tasks[i].idname, tasks[j].idname = name2, tasks[i].idname
        for field in ['finished', 'boxes', 'prop_photo', 'prop_occluded', 'prop_art', 'prop_st']:
            attr1, attr2 = getattr(tasks[j], field), getattr(tasks[i], field)
            setattr(tasks[i], field, attr1)
            setattr(tasks[j], field, attr2)
        tasks[i].save()
        tasks[j].save()
