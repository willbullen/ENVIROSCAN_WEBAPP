# Generated by Django 3.2.11 on 2022-01-28 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0025_autosonde_ground_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Stage_1',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Stage_2',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Stage_3',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Stage_4',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Stage_5',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Stage_6',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Stage_7',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='autosonde_soundings',
            name='Data_Type',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]