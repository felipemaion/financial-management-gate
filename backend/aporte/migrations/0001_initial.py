# Generated by Django 2.2 on 2019-04-15 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('date', models.DateField(verbose_name='Date')),
                ('final_date', models.DateField(null=True, verbose_name='Final Date')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
