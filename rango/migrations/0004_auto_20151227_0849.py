# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_auto_20151222_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='last_visit',
            field=models.DateField(blank=True, null=True),
        ),
    ]
