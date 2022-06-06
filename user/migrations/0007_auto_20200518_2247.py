# Generated by Django 3.0.2 on 2020-05-18 22:47

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_biodatamodel_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='gallery_image',
            field=models.ImageField(default='image.png', upload_to=user.models.Gallery.image_directory_path),
        ),
    ]