# Generated by Django 3.0.3 on 2020-07-03 22:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0011_auto_20200703_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='display',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]