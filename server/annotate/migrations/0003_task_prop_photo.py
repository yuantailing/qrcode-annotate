# Generated by Django 3.1.7 on 2021-03-06 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0002_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='prop_photo',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
