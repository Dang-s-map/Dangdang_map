# Generated by Django 4.0.6 on 2022-08-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dang', '0003_favorite_remove_accomodation_like_remove_cafe_like_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='favorite',
        ),
        migrations.AddField(
            model_name='favorite',
            name='already_like',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='favorite',
            name='like',
            field=models.TextField(default='<i class="far fa-heart"></i>'),
        ),
    ]
