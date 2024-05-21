# Generated by Django 5.0.6 on 2024-05-21 12:18

import cafe.libs.gen_id
import django.contrib.auth.models
import django.utils.timezone
import functools
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.CharField(default=functools.partial(cafe.libs.gen_id.gen_id, *(cafe.libs.gen_id.IDType['PUBLISHER'],), **{}), max_length=24, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RDLevel',
            fields=[
                ('id', models.CharField(default=functools.partial(cafe.libs.gen_id.gen_id, *(cafe.libs.gen_id.IDType['RD_LEVEL'],), **{}), max_length=24, primary_key=True, serialize=False)),
                ('song', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(default=functools.partial(cafe.libs.gen_id.gen_id, *(cafe.libs.gen_id.IDType['USER'],), **{}), max_length=24, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
