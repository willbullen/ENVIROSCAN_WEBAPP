# Generated by Django 3.2.11 on 2022-04-07 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0036_cmms_jobs_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cmms_jobs',
            old_name='author',
            new_name='Author',
        ),
    ]