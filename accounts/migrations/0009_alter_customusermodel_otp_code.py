# Generated by Django 5.0.4 on 2024-09-01 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customusermodel_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='otp_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]