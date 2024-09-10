# Generated by Django 5.0.4 on 2024-09-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_counseling_agent_status_session_agent_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='counseling',
            name='city',
            field=models.CharField(blank=True, choices=[('teh', 'تهران'), ('krj', 'کرج')], default='تهران', max_length=30, null=True, verbose_name='شهر'),
        ),
        migrations.AddField(
            model_name='counseling',
            name='district',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='محله'),
        ),
        migrations.AddField(
            model_name='session',
            name='district',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='محله'),
        ),
        migrations.AddField(
            model_name='visit',
            name='district',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='محله'),
        ),
    ]