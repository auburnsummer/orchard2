# Generated by Django 5.0.7 on 2024-10-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0018_rdlevel_artist_rdlevel_artist_tokens_rdlevel_authors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rdlevel',
            name='rdzip_url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]