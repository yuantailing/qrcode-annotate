import io
import json
import os
import PIL.Image

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import include, path, reverse

from .models import *

# Create your views here.

def index(request):
    return render(request, 'annotate/index.html')

def task(request, id):
    task = get_object_or_404(Task.objects, id=id)
    token = Token.objects.filter(secret=request.session.get('annotate_token', '')).first()
    if token:
        writable = token.task_id_start <= id <= token.task_id_end
    else:
        writable = False
    if request.method == 'POST' and writable:
        task.boxes = json.dumps(json.loads(request.POST['boxes']))
        task.finished = True
        task.prop_photo = int(request.POST['prop_photo'])
        task.prop_occluded = int(request.POST['prop_occluded'])
        task.prop_art = int(request.POST['prop_art'])
        task.prop_st = int(request.POST['prop_st'])
        with transaction.atomic():
            Log.objects.create(task=task, post_body=request.body)
            task.save()
        return HttpResponse('ok')
    return render(request, 'annotate/task.html', {'task': task, 'token': token, 'writable': writable, 'boxes': task.boxes or [], 'previous': reverse('annotate:task', args=[task.id - 1]), 'next': reverse('annotate:task', args=[task.id + 1])})

def getimage(request, id):
    task = get_object_or_404(Task.objects, id=id)
    path1 = f'{webimgs_root_dir}/{task.idname}'
    paths = [f'{path1}.jpeg', f'{path1}.png', f'{path1}.gif']
    for path in paths:
        if os.path.isfile(path):
            img = PIL.Image.open(path)
    jpeg = img.convert('RGB')
    bytesio = io.BytesIO()
    jpeg.save(bytesio, "JPEG", quality=90)
    return HttpResponse(bytesio.getvalue(), content_type='image/jpeg')

def tokenlogin(request):
    token = request.POST['token']
    request.session['annotate_token'] = token
    return HttpResponse('')
