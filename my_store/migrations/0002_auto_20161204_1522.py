# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-04 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
