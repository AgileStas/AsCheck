# Generated by Django 5.1.1 on 2024-11-07 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0013_host_active_usbstor_active_usbstor_person_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usbstor',
            name='note',
            field=models.TextField(default=''),
        ),
    ]
