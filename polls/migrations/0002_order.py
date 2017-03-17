# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('weekday', models.IntegerField(default=0)),
                ('point_x', models.CharField(max_length=20)),
                ('point_y', models.CharField(max_length=20)),
                ('order_date', models.DateTimeField()),
            ],
        ),
    ]
