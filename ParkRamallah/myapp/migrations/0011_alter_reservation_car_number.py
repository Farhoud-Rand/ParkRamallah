# Generated by Django 5.0.3 on 2024-04-30 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_reservation_car_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='car_number',
            field=models.CharField(max_length=20),
        ),
    ]