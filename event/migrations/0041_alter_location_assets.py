# Generated by Django 3.2.3 on 2021-07-25 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0040_auto_20210725_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='Assets',
            field=models.ManyToManyField(null=True, to='event.Asset'),
        ),
    ]