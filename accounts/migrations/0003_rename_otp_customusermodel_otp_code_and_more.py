# Generated by Django 5.0.4 on 2024-04-11 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_profile_mobile_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customusermodel',
            old_name='otp',
            new_name='otp_code',
        ),
        migrations.RenameField(
            model_name='customusermodel',
            old_name='otp_creation_time',
            new_name='otp_code_datetime_created',
        ),
    ]
