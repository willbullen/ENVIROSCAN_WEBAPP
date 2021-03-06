# Generated by Django 3.2.11 on 2022-01-16 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20220116_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_Name', models.CharField(max_length=50)),
                ('Category_Description', models.CharField(max_length=200)),
                ('Client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.clients')),
            ],
            options={
                'ordering': ['Category_Name'],
            },
        ),
    ]
