# Generated by Django 5.0.3 on 2024-04-24 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_park_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='park',
            name='name',
            field=models.CharField(default='s', max_length=100),
        ),
    ]