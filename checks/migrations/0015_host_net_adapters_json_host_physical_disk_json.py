# Generated by Django 5.1.1 on 2025-03-15 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0014_usbstor_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='net_adapters_json',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='physical_disk_json',
            field=models.JSONField(null=True),
        ),
    ]
