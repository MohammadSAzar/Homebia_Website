import jdatetime
from django import template

register = template.Library()

PERSIAN_MONTH_NAMES = {
    'Farvardin': 'فروردین',
    'Ordibehesht': 'اردیبهشت',
    'Khordad': 'خرداد',
    'Tir': 'تیر',
    'Mordad': 'مرداد',
    'Shahrivar': 'شهریور',
    'Mehr': 'مهر',
    'Aban': 'آبان',
    'Azar': 'آذر',
    'Dey': 'دی',
    'Bahman': 'بهمن',
    'Esfand': 'اسفند'
}

@register.filter
def shamsi_date(datetime):
    if datetime:
        jalali_datetime = jdatetime.datetime.fromgregorian(datetime=datetime)
        persian_month = PERSIAN_MONTH_NAMES[jalali_datetime.strftime('%B')]
        formatted_date = jalali_datetime.strftime(f'%d {persian_month} %Y')
        formatted_time = jalali_datetime.strftime('%H و %M دقیقه')
        formatted_datetime = f"{formatted_date} - ساعت {formatted_time}"
        return formatted_datetime
    return ''

