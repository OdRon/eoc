# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-28 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mytimetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=1000)),
                ('from_date', models.CharField(default=b'', max_length=500)),
                ('to_date', models.CharField(default=b'', max_length=500)),
                ('deleted', models.CharField(default=b'N', max_length=20)),
            ],
        ),
    ]
