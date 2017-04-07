# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 02:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ws_interlace.models


class Migration(migrations.Migration):

    dependencies = [
        ('ws_interlace', '0018_remove_answer_student_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=ws_interlace.models.get_image_path)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='ws_interlace.Answer')),
            ],
        ),
    ]
