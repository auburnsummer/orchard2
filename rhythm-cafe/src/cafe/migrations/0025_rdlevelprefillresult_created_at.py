# Generated by Django 5.0.7 on 2024-10-09 14:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0024_alter_rdlevel_sha1'),
    ]

    operations = [
        migrations.AddField(
            model_name='rdlevelprefillresult',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
