# Generated by Django 3.2.3 on 2021-06-02 13:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=400)),
                ('featured_image', models.ImageField(blank=True, upload_to='covers/')),
                ('Latitude', models.CharField(max_length=200)),
                ('Google_maps_link', models.CharField(max_length=200)),
                ('Plus_code', models.CharField(max_length=200)),
                ('ASSETS_TYPE', models.CharField(choices=[('IOS', 'IOS'), ('ANDROID', 'Android')], default='IOS', max_length=8)),
            ],
        ),
    ]
