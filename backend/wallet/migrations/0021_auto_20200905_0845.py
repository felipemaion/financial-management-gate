# Generated by Django 3.0.3 on 2020-09-05 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0020_auto_20200905_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='date',
            field=models.DateTimeField(verbose_name='date'),
        ),
    ]
