# Generated by Django 3.0.3 on 2020-05-04 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_instrument_moviment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviment',
            name='total_costs',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='costs'),
        ),
    ]
