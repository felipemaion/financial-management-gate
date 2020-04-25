# Generated by Django 2.2 on 2019-07-03 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aporte', '0004_auto_20190416_0554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('daily_factor', models.DecimalField(decimal_places=10, max_digits=11, verbose_name='Daily Fator')),
            ],
        ),
    ]
