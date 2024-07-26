# Generated by Django 5.0.4 on 2024-07-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='guaranteed_gain_percent',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Guaranteed gain percent'),
        ),
    ]
