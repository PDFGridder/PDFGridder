# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Untitled', max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('star', models.BooleanField(default=False)),
                ('hash', models.CharField(max_length=40, null=True, blank=True)),
                ('width', models.FloatField(default=210)),
                ('width_unit', models.CharField(default=b'mm', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('height', models.FloatField(default=297)),
                ('height_unit', models.CharField(default=b'mm', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('margin_left', models.FloatField(default=5, verbose_name=b'Left')),
                ('margin_left_unit', models.CharField(default=b'mm', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('margin_right', models.FloatField(default=5, verbose_name=b'Right')),
                ('margin_right_unit', models.CharField(default=b'mm', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('margin_top', models.FloatField(default=5, verbose_name=b'Top')),
                ('margin_top_unit', models.CharField(default=b'mm', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('margin_bottom', models.FloatField(default=5, verbose_name=b'Bottom')),
                ('margin_bottom_unit', models.CharField(default=b'mm', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('columns', models.IntegerField(default=7)),
                ('columns_gutter', models.FloatField(default=3)),
                ('columns_gutter_unit', models.CharField(default=b'mm', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('baseline', models.FloatField(default=15)),
                ('baseline_unit', models.CharField(default=b'pt', max_length=2, choices=[(b'in', b'inches'), (b'mm', b'millimeters'), (b'px', b'pixels'), (b'pt', b'points')])),
                ('grid', models.FileField(null=True, upload_to=b'grids', blank=True)),
                ('columns_color', models.CharField(default=b'#eeeeee', max_length=7)),
                ('columns_opacity', models.FloatField(default=1.0)),
                ('baseline_color', models.CharField(default=b'#c0c0c0', max_length=7)),
                ('baseline_opacity', models.FloatField(default=1.0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_spread', models.BooleanField(default=False, verbose_name=b'Facing pages')),
                ('session_key', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
