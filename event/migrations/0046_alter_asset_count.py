# Generated by Django 3.2.3 on 2021-07-28 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0045_auto_20210728_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='count',
            field=models.IntegerField(null=True),
        ),
    ]
