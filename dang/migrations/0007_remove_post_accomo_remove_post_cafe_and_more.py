# Generated by Django 4.0.6 on 2022-08-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dang', '0006_alter_post_postimage_alter_post_posttype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='accomo',
        ),
        migrations.RemoveField(
            model_name='post',
            name='cafe',
        ),
        migrations.RemoveField(
            model_name='post',
            name='place',
        ),
        migrations.AddField(
            model_name='post',
            name='placeId',
            field=models.IntegerField(null=True),
        ),
    ]
