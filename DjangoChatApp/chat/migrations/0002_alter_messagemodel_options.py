# Generated by Django 4.1.2 on 2022-10-19 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagemodel',
            options={'ordering': ['updated', 'created']},
        ),
    ]