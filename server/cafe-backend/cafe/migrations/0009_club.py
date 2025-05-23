# Generated by Django 5.1.4 on 2025-01-19 06:59

import cafe.models.id_utils
import rules.contrib.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0008_alter_user_theme_preference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.CharField(default=cafe.models.id_utils.generate_club_id, max_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
