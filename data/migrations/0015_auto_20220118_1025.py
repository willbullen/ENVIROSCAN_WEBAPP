# Generated by Django 3.2.11 on 2022-01-18 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20220116_2201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nodes',
            options={'ordering': ['Node_ID']},
        ),
        migrations.AlterField(
            model_name='clients',
            name='Client_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='node_category',
            name='Category_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='node_location',
            name='Location_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='node_site',
            name='Site_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='node_type',
            name='Type_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='Node_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='Node_ID',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]