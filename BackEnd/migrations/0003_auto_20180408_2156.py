# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-08 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0002_news_tarifs_uchastok'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uchastok',
            name='parentid',
            field=models.IntegerField(default=0),
        ),
    ]
