# Generated by Django 3.0.3 on 2020-04-29 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aporte', '0010_instrument_moviment_movimentwallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instrument',
            old_name='crpn',
            new_name='crpNm',
        ),
        migrations.AlterField(
            model_name='instrument',
            name='mktNm',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='mktNm'),
        ),
    ]