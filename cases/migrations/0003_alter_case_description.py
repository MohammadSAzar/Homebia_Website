# Generated by Django 5.0.4 on 2024-07-26 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_alter_case_guaranteed_gain_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
