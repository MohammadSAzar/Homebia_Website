# Generated by Django 5.0.4 on 2024-09-07 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_counseling_counseling_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counseling',
            name='counseling_type',
            field=models.CharField(choices=[('ip', 'حضوری'), ('op', 'تلفنی'), ('oc', 'چتی')], default='oc', max_length=30, verbose_name='نوع مشاوره'),
        ),
    ]
