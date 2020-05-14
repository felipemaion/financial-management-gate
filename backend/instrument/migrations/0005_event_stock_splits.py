# Generated by Django 3.0.3 on 2020-05-13 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0004_auto_20200513_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='stock_splits',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20, verbose_name='stock splits'),
            preserve_default=False,
        ),
    ]
