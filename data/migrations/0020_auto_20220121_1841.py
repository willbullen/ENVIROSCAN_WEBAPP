# Generated by Django 3.2.11 on 2022-01-21 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0019_alter_nodes_node_device_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodes',
            name='Asset_Status_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='Data_Status_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='Node_Status_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='Server_Status_Description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]