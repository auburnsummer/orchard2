# Generated by Django 5.0.7 on 2024-07-24 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0014_rdlevelprefillresult_club_rdlevelprefillresult_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='rdlevelprefillresult',
            name='errors',
            field=models.TextField(default=''),
        ),
    ]
