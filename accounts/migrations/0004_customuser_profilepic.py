# Generated by Django 3.2.3 on 2021-06-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_customuser_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profilePic',
            field=models.ImageField(blank=True, upload_to='profilePic/'),
        ),
    ]
