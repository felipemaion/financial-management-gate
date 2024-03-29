# Generated by Django 3.0.3 on 2020-09-07 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0022_auto_20200811_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dividend',
            name='adjusted_value',
            field=models.DecimalField(decimal_places=10, max_digits=20, verbose_name='adjusted value'),
        ),
        migrations.AlterField(
            model_name='dividend',
            name='value',
            field=models.DecimalField(decimal_places=10, max_digits=20, verbose_name='value'),
        ),
    ]
