# Generated by Django 5.0.4 on 2024-09-01 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0002_alter_agentcustomusermodel_complete_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentcustomusermodel',
            name='otp_code',
            field=models.PositiveIntegerField(blank=True, max_length=5, null=True),
        ),
    ]
