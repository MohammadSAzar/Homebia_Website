# Generated by Django 5.0.4 on 2024-07-10 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restates', '0013_rentfile_rent_file_code_salefile_sale_file_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentfile',
            old_name='rent_file_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='salefile',
            old_name='sale_file_code',
            new_name='code',
        ),
    ]
