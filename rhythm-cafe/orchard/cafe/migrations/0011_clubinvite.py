# Generated by Django 5.0.6 on 2024-06-21 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0010_alter_clubmembership_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin')], max_length=10)),
                ('expiry', models.DateTimeField()),
                ('code', models.CharField(max_length=100)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.club')),
            ],
        ),
    ]