# Generated by Django 3.2.3 on 2021-07-28 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0044_asset_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='latitude1',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='longitude1',
        ),
        migrations.RemoveField(
            model_name='location',
            name='Assets',
        ),
        migrations.AddField(
            model_name='asset',
            name='Locations',
            field=models.ManyToManyField(null=True, to='event.Location'),
        ),
    ]
