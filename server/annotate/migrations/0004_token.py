# Generated by Django 3.1.7 on 2021-03-06 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0003_task_prop_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.CharField(db_index=True, max_length=64, unique=True)),
                ('task_id_start', models.IntegerField()),
                ('task_id_end', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]