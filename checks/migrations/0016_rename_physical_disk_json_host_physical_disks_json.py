# Generated by Django 5.1.1 on 2025-03-15 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0015_host_net_adapters_json_host_physical_disk_json'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='physical_disk_json',
            new_name='physical_disks_json',
        ),
    ]
