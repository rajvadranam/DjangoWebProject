# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-13 15:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20181113_0903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bks',
            name='a_id',
        ),
        migrations.RemoveField(
            model_name='bks',
            name='dpt_id',
        ),
        migrations.RemoveField(
            model_name='border',
            name='b_id',
        ),
        migrations.RemoveField(
            model_name='border',
            name='cwid',
        ),
        migrations.RemoveField(
            model_name='border',
            name='i_id',
        ),
        migrations.RemoveField(
            model_name='border',
            name='lb_id',
        ),
        migrations.RemoveField(
            model_name='bowed',
            name='b_id',
        ),
        migrations.RemoveField(
            model_name='bowed',
            name='cwid',
        ),
        migrations.RemoveField(
            model_name='bowed',
            name='i_id',
        ),
        migrations.RemoveField(
            model_name='invt',
            name='i_id',
        ),
        migrations.RemoveField(
            model_name='libmem',
            name='cwid',
        ),
        migrations.RemoveField(
            model_name='libmem',
            name='dpt_id',
        ),
        migrations.RemoveField(
            model_name='librn',
            name='dpt_id',
        ),
        migrations.RemoveField(
            model_name='stud',
            name='dpt_id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Atr',
        ),
        migrations.DeleteModel(
            name='Bks',
        ),
        migrations.DeleteModel(
            name='Border',
        ),
        migrations.DeleteModel(
            name='Bowed',
        ),
        migrations.DeleteModel(
            name='Dept',
        ),
        migrations.DeleteModel(
            name='Invt',
        ),
        migrations.DeleteModel(
            name='Libmem',
        ),
        migrations.DeleteModel(
            name='Librn',
        ),
        migrations.DeleteModel(
            name='Stud',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
