# Generated by Django 4.1 on 2022-08-14 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dang', '0002_alter_accomodation_options_alter_medical_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='star',
            field=models.CharField(max_length=100, null=True),
        ),
    ]