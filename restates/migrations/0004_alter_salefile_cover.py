# Generated by Django 5.0.4 on 2024-06-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restates', '0003_remove_salefile_unique_url_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salefile',
            name='cover',
            field=models.ImageField(blank=True, upload_to='files/', verbose_name='File cover'),
        ),
    ]
