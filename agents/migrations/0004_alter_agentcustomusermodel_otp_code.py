# Generated by Django 5.0.4 on 2024-09-01 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_alter_agentcustomusermodel_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentcustomusermodel',
            name='otp_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
