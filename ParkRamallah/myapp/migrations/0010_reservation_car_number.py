# Generated by Django 5.0.3 on 2024-04-30 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_reservation_delete_nreservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='car_number',
            field=models.CharField(default='00000000', max_length=20),
        ),
    ]
