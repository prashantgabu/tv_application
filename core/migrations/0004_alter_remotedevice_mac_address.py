# Generated by Django 3.2 on 2022-09-04 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remotedevice_mac_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remotedevice',
            name='mac_address',
            field=models.CharField(blank=True, max_length=300, null=True, unique=True, verbose_name='MAC Address'),
        ),
    ]
