# Generated by Django 3.2.3 on 2021-06-02 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20210602_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='Expiry_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='Expiry_time',
            field=models.TimeField(null=True),
        ),
    ]
