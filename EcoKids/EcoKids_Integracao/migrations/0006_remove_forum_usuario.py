# Generated by Django 4.2.7 on 2024-04-21 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EcoKids_Integracao', '0005_rename_mural_forum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='usuario',
        ),
    ]
