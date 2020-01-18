# Generated by Django 2.2 on 2019-08-12 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aporte', '0007_auto_20190703_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ativo',
            fields=[
                ('aporte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aporte.Aporte')),
            ],
            bases=('aporte.aporte',),
        ),
        migrations.CreateModel(
            name='TipoAtivo',
            fields=[
                ('grupo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aporte.Grupo')),
                ('tipo', models.CharField(max_length=60, unique=True)),
            ],
            bases=('aporte.grupo',),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]