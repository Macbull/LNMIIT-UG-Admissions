# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ug', '0002_remove_admissiondetail_no_of_rounds'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='date_applied',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 5, 20, 50, 375958, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
