# Generated by Django 5.0.4 on 2024-07-27 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0006_remove_caseorder_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='caseorder',
            name='notes',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Notes'),
        ),
    ]
