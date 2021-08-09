# Generated by Django 3.2.3 on 2021-07-13 09:44

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0036_auto_20210711_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='Multi_Locations',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=100, null=True), size=None), null=True, size=255),
        ),
        migrations.AlterField(
            model_name='asset',
            name='multi_uploads',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.FileField(blank=True, upload_to='covers/'), null=True, size=None),
        ),
    ]