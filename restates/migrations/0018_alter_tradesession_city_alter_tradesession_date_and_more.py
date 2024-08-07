# Generated by Django 5.0.4 on 2024-07-17 15:55

import django.db.models.deletion
import services.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restates', '0017_alter_tradesession_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradesession',
            name='city',
            field=models.CharField(choices=[('thrn', 'تهران'), ('karj', 'کرج'), ('ands', 'اندیشه'), ('shrr', 'شهریار'), ('prds', 'پردیس'), ('prnd', 'پرند')], default='thrn', max_length=30, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='date',
            field=models.CharField(choices=services.models.next_seven_days_shamsi, max_length=200, verbose_name='تاریخ برگزاری'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان و تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='is_followed',
            field=models.CharField(choices=[('is', 'هست'), ('isnt', 'نیست')], default='isnt', max_length=200, verbose_name='آیا معامله نیاز به پیگیری دارد؟'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='is_paid',
            field=models.CharField(choices=[('is', 'هست'), ('isnt', 'نیست')], default='isnt', max_length=200, verbose_name='آیا پرداخت کمیسیون انجام شده است؟'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='is_success',
            field=models.CharField(choices=[('is', 'هست'), ('isnt', 'نیست')], default='isnt', max_length=200, verbose_name='آیا معامله موفقیت\u200cآمیز بود؟'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='location',
            field=models.CharField(choices=[('ours', 'به میزبانی هومبابا'), ('yours', 'در محل پیشنهادی شما')], max_length=30, verbose_name='مکان'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='name_and_family',
            field=models.CharField(max_length=200, verbose_name='نام و نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='ours',
            field=models.CharField(choices=[('is', 'هست'), ('isnt', 'نیست')], max_length=30, verbose_name='آیا فایل از آگهی\u200cهای هومبابا است؟'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='تلفن همراه منتشر کننده'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='rent_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='کد آگهی اجاره'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='rent_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trades', to='restates.rentfile', verbose_name='آگهی اجاره'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='sale_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='کد آگهی فروش'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='sale_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trades', to='restates.salefile', verbose_name='آگهی\u200c فروش'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='time',
            field=models.CharField(choices=[('mg', 'صبح'), ('nn', 'ظهر'), ('eg', 'عصر'), ('nt', 'شب')], max_length=200, verbose_name='زمان برگزاری'),
        ),
        migrations.AlterField(
            model_name='tradesession',
            name='trade_type',
            field=models.CharField(choices=[('sale', 'فروش'), ('rent', 'اجاره')], max_length=30, verbose_name='نوع معامله'),
        ),
    ]
