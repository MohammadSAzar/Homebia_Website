# Generated by Django 5.0.4 on 2024-09-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_alter_counseling_counseling_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counseling',
            name='district',
        ),
        migrations.AlterField(
            model_name='counseling',
            name='city',
            field=models.CharField(blank=True, default='تهران', max_length=30, null=True, verbose_name='شهر'),
        ),
    ]
