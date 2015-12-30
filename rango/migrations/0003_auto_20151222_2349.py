# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20151201_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='first_visit',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='page',
            name='last_visit',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
