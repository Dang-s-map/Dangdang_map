# Generated by Django 3.2.15 on 2022-08-11 07:16

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='사용자 아이디')),
                ('password', models.CharField(max_length=64, null=True, verbose_name='사용자 비밀번호')),
                ('email', models.EmailField(max_length=128, null=True, verbose_name='사용자 이메일')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('star', models.CharField(max_length=100, null=True)),
                ('link1', models.TextField(null=True)),
                ('link2', models.TextField(null=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('desc', models.CharField(max_length=255, null=True)),
                ('img', models.ImageField(null=True, upload_to='')),
                ('mapx', models.CharField(max_length=100, null=True)),
                ('mapy', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('menuInfo', models.TextField(null=True)),
                ('hourInfo', models.TextField(null=True)),
                ('link1', models.TextField(null=True)),
                ('desc', models.TextField(null=True)),
                ('img', models.ImageField(null=True, upload_to='')),
                ('mapx', models.CharField(max_length=100, null=True)),
                ('mapy', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='찜')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locationName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('star', models.CharField(max_length=100, null=True)),
                ('link1', models.TextField(null=True)),
                ('link2', models.TextField(null=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('desc', models.TextField(null=True)),
                ('img', models.ImageField(null=True, upload_to='')),
                ('mapx', models.CharField(max_length=100, null=True)),
                ('mapy', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postType', models.CharField(max_length=100)),
                ('postGood', models.CharField(max_length=100)),
                ('postBad', models.CharField(max_length=100)),
                ('postImage', models.CharField(max_length=100)),
                ('ranking', models.CharField(max_length=100)),
                ('accomos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dang.accomodation')),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dang.cafe')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dang.location')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dang.place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dang.user')),
            ],
        ),
        migrations.CreateModel(
            name='Medical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicalName', models.CharField(max_length=100)),
                ('medicalPhone', models.CharField(max_length=100)),
                ('medicalAddress', models.CharField(max_length=100)),
                ('medicalLocation', models.CharField(max_length=100)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dang.location')),
            ],
        ),
    ]
