# Generated by Django 5.0.4 on 2024-05-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_book_blogcomment_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomment',
            name='recommend',
        ),
        migrations.RemoveField(
            model_name='blogcomment',
            name='user',
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='name',
            field=models.CharField(default='خواننده هومبیا', max_length=40),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='is_active',
            field=models.BooleanField(choices=[('pr', 'Proved'), ('pd', 'Pending'), ('rj', 'Rejected')], default='pd'),
        ),
    ]