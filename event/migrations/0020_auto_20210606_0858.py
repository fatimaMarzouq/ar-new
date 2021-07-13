# Generated by Django 3.2.3 on 2021-06-06 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0019_auto_20210606_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='Location',
        ),
        migrations.AddField(
            model_name='location',
            name='Events',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Events', to='event.event'),
        ),
    ]