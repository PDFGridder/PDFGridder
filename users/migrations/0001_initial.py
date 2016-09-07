# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import avatar.models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_avatar', models.ImageField(max_length=1024, null=True, upload_to=avatar.models.avatar_file_path, blank=True)),
                ('full_name', models.CharField(max_length=200, blank=True)),
                ('bio', models.CharField(max_length=500, blank=True)),
                ('city', models.CharField(max_length=100, blank=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('stripe_customer_id', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
