# Generated by Django 5.0.3 on 2024-05-19 03:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcoKids_Integracao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='total_pontuacao',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='UsuarioTarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realizada', models.BooleanField(default=False)),
                ('tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EcoKids_Integracao.tarefa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EcoKids_Integracao.usuario')),
            ],
        ),
    ]