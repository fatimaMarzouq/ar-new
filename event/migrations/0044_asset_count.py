# Generated by Django 3.2.3 on 2021-07-27 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0043_auto_20210725_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='count',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
