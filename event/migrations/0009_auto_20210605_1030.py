# Generated by Django 3.2.3 on 2021-06-05 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20210605_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='Radius',
            field=models.DecimalField(decimal_places=10, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='Locations',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Locations', to='event.asset'),
        ),
    ]
