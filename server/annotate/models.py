from django.db import models

# Create your models here.

webimgs_root_dir = '../webimgs'

class Task(models.Model):
    idname = models.CharField(max_length=64, unique=True, db_index=True)
    finished = models.IntegerField(db_index=True)
    boxes = models.TextField()
    prop_photo = models.IntegerField()
    prop_occluded = models.IntegerField()
    prop_art = models.IntegerField()
    prop_st = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Log(models.Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    post_body = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Token(models.Model):
    secret = models.CharField(max_length=64, unique=True, db_index=True)
    task_id_start = models.IntegerField()
    task_id_end = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
