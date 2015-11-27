# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ug', '0003_application_date_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='allotedseat',
            name='valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='allotedseat',
            unique_together=set([('councelling_round', 'application')]),
        ),
    ]
