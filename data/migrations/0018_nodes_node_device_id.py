# Generated by Django 3.2.11 on 2022-01-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_picarro_data_node_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodes',
            name='Node_Device_ID',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
