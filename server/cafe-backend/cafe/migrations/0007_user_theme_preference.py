# Generated by Django 5.1.4 on 2025-01-16 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0006_user_date_joined_user_first_name_user_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='theme_preference',
            field=models.CharField(choices=[('light', 'Light'), ('dark', 'Dark')], default='light', max_length=100),
            preserve_default=False,
        ),
    ]
