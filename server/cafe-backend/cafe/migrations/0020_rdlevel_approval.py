# Generated by Django 5.2 on 2025-04-29 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0019_rdlevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='rdlevel',
            name='approval',
            field=models.IntegerField(default=0),
        ),
    ]
