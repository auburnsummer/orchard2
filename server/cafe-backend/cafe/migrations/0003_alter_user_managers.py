# Generated by Django 5.1.4 on 2024-12-29 05:44

import cafe.models.user
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_alter_user_email_alter_user_id_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', cafe.models.user.CafeUserManager()),
            ],
        ),
    ]
