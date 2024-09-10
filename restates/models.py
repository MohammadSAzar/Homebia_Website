import random
import string
from jdatetime import date, timedelta

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext as _

from . import choices
from services.models import next_seven_days_shamsi, statuses, times, session_price_value


# --------------------------------- Locations ---------------------------------
class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name


# --------------------------------- Files ---------------------------------
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def generate_unique_code():
    return ''.join(random.choices(string.digits + string.digits, k=6))


class SaleFile(models.Model):
    # location fields
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_files', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_files', verbose_name=_('City'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_files', verbose_name=_('District'))
    # general characteristics
    price = models.PositiveBigIntegerField(verbose_name=_('Price'))
    room = models.CharField(max_length=15, choices=choices.rooms, verbose_name=_('Number of Rooms'))
    area = models.PositiveIntegerField(verbose_name=_('Area'))
    age = models.CharField(max_length=15, choices=choices.ages, default='1', verbose_name=_('Age of Apartment'))
    document = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Document'))
    level = models.CharField(max_length=15, choices=choices.levels, verbose_name=_('Level'))
    parking = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Parking'))
    elevator = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Elevator'))
    warehouse = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Warehouse'))
    cover = models.ImageField(upload_to='files/covers/', blank=True, verbose_name=_('File cover'))
    cover2 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 2'))
    cover3 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 3'))
    cover4 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 4'))
    # optional
    direction = models.CharField(max_length=15, choices=choices.directions, null=True, blank=True, verbose_name=_('File Direction'))
    file_levels = models.CharField(max_length=15, choices=choices.levels, null=True, blank=True, verbose_name=_('File Levels Number'))
    aparts_per_level = models.CharField(max_length=15, choices=choices.aparts_per_level, null=True, blank=True, verbose_name=_('Apartments per Level'))
    restoration = models.CharField(max_length=15, choices=choices.restorations, null=True, blank=True, verbose_name=_('Restoration'))
    bench_stove = models.CharField(max_length=15, choices=choices.booleans, null=True, blank=True, verbose_name=_('Bench Stove'))
    balcony = models.CharField(max_length=15, choices=choices.booleans, null=True, blank=True, verbose_name=_('Balcony'))
    toilet = models.CharField(max_length=15, choices=choices.toilets, null=True, blank=True, verbose_name=_('Toilet'))
    hot_water = models.CharField(max_length=15, choices=choices.hot_water, null=True, blank=True, verbose_name=_('Hot Water System'))
    cooling = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Cooling System'))
    heating = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Heating System'))
    floor = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Floor Type'))
    # general information
    title = models.CharField(max_length=230, verbose_name=_('File Title'))
    description = models.TextField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True, allow_unicode=True)
    unique_url_id = models.CharField(max_length=20, null=True, unique=True, blank=True)
    code = models.CharField(max_length=6, null=True, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=choices.statuses, default='pen')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_expired = models.DateTimeField(blank=True, null=True)
    # personal information
    provider_name = models.CharField(max_length=50, verbose_name=_('Provider Name'))
    phone_number_for_contact = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Provider Phone Number'))
    provider_national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Provider National Code'))
    owner_national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Owner National Code'))
    file_postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('File Postal Code'))

    @property
    def price_per_meter(self):
        return int(self.price/self.area)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_status = SaleFile.objects.get(pk=self.pk).status
            if old_status == 'pen' and self.status == 'acc':
                self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        else:
            if self.status == 'acc':
                self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        if not self.unique_url_id:
            self.unique_url_id = generate_unique_id()
        if not self.code:
            self.code = generate_unique_code()
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(SaleFile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} / {self.unique_url_id}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('sale_file_detail', args=[self.slug, self.unique_url_id])


class RentFile(models.Model):
    # location fields
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='rent_files', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='rent_files', verbose_name=_('City'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='rent_files', verbose_name=_('District'))
    # general characteristics
    price_deposit = models.PositiveBigIntegerField(verbose_name=_('Deposit Price'))
    price_rent = models.PositiveBigIntegerField(verbose_name=_('Rent Price'))
    convertable = models.CharField(max_length=15, choices=choices.beings, verbose_name=_('Convertable'))
    room = models.CharField(max_length=15, choices=choices.rooms, verbose_name=_('Number of Rooms'))
    area = models.PositiveIntegerField(verbose_name=_('Area'))
    age = models.CharField(max_length=15, choices=choices.ages, default='1', verbose_name=_('Age of Apartment'))
    document = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Document'))
    level = models.CharField(max_length=15, choices=choices.levels, verbose_name=_('Level'))
    parking = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Parking'))
    elevator = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Elevator'))
    warehouse = models.CharField(max_length=15, choices=choices.booleans, verbose_name=_('Warehouse'))
    cover = models.ImageField(upload_to='files/covers/', blank=True, verbose_name=_('File cover'))
    cover2 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 2'))
    cover3 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 3'))
    cover4 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 4'))
    # optional
    direction = models.CharField(max_length=15, choices=choices.directions, null=True, blank=True, verbose_name=_('File Direction'))
    file_levels = models.CharField(max_length=15, choices=choices.levels, null=True, blank=True, verbose_name=_('File Levels Number'))
    aparts_per_level = models.CharField(max_length=15, choices=choices.aparts_per_level, null=True, blank=True, verbose_name=_('Apartments per Level'))
    restoration = models.CharField(max_length=15, choices=choices.restorations, null=True, blank=True, verbose_name=_('Restoration'))
    bench_stove = models.CharField(max_length=15, choices=choices.booleans, null=True, blank=True, verbose_name=_('Bench Stove'))
    balcony = models.CharField(max_length=15, choices=choices.booleans, null=True, blank=True, verbose_name=_('Balcony'))
    toilet = models.CharField(max_length=15, choices=choices.toilets, null=True, blank=True, verbose_name=_('Toilet'))
    hot_water = models.CharField(max_length=15, choices=choices.hot_water, null=True, blank=True, verbose_name=_('Hot Water System'))
    cooling = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Cooling System'))
    heating = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Heating System'))
    floor = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Floor Type'))
    # general information
    title = models.CharField(max_length=230, verbose_name=_('File Title'))
    description = models.TextField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True, allow_unicode=True)
    unique_url_id = models.CharField(max_length=20, null=True, unique=True, blank=True)
    code = models.CharField(max_length=6, null=True, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=choices.statuses, default='pen')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_expired = models.DateTimeField(blank=True, null=True)
    # personal information
    provider_name = models.CharField(max_length=50, verbose_name=_('Provider Name'))
    phone_number_for_contact = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Provider Phone Number'))
    provider_national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Provider National Code'))
    owner_national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Owner National Code'))
    file_postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('File Postal Code'))

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_status = RentFile.objects.get(pk=self.pk).status
            if old_status == 'pen' and self.status == 'acc':
                self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        else:
            if self.status == 'acc':
                self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        if not self.unique_url_id:
            self.unique_url_id = generate_unique_id()
        if not self.code:
            self.code = generate_unique_code()
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(RentFile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} / {self.unique_url_id}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('rent_file_detail', args=[self.slug, self.unique_url_id])


# --------------------------------- Trade ---------------------------------
trade_cities = [
    ('thrn', _('Tehran')),
    ('karj', _('Karaj')),
    ('ands', _('Andisheh')),
    ('shrr', _('Shahriar')),
    ('prds', _('Pardis')),
    ('prnd', _('Parand')),
]
types = [
    ('sale', _('Sale')),
    ('rent', _('Rent')),
    ]
locations = [
    ('ours', _('Ours')),
    ('yours', _('Yours')),
]
noyes = [
    ('yes', _('Yes')),
    ('no', _('No')),
]
beings = [
    ('is', _('Is')),
    ('isnt', _('Is Not')),
]


class TradeSession(models.Model):
    # Constants (imported)
    DATES = next_seven_days_shamsi
    TIMES = times
    STATUSES = statuses
    # Constants (here)
    CITIES = trade_cities
    LOCATIONS = locations
    TYPES = types
    BEINGS = beings
    NOYES = noyes
    # Session
    city = models.CharField(max_length=30, choices=CITIES, default='thrn', verbose_name=_('City'))
    district = models.CharField(max_length=30, default='', blank=True, null=True, verbose_name=_('District'))
    location = models.CharField(max_length=30, choices=LOCATIONS, verbose_name=_('Location'))
    date = models.CharField(max_length=200, choices=DATES, verbose_name=_('Date of Session'))
    time = models.CharField(max_length=200, choices=TIMES, verbose_name=_('Time of Session'))
    name_and_family = models.CharField(max_length=200, verbose_name=_('First Name and Family'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('First Phone Number'))
    # File
    trade_type = models.CharField(max_length=30, choices=TYPES, verbose_name=_('Trade Type'))
    ours = models.CharField(max_length=30, choices=BEINGS, verbose_name=_('Is trade ours?'))
    sale_file = models.ForeignKey(SaleFile, on_delete=models.SET_NULL, null=True, blank=True, related_name='trades', verbose_name=_('Sale File'))
    sale_code = models.CharField(max_length=6, null=True, blank=True, verbose_name=_('Sale File Code'))
    rent_file = models.ForeignKey(RentFile, on_delete=models.SET_NULL, null=True, blank=True, related_name='trades', verbose_name=_('Rent File'))
    rent_code = models.CharField(max_length=6, null=True, blank=True, verbose_name=_('Rent File Code'))
    # Result
    is_success = models.CharField(max_length=200, choices=NOYES, default='no', verbose_name=_('Is trade successful?'))
    is_followed = models.CharField(max_length=200, choices=NOYES, default='no', verbose_name=_('Is trade has follow-up?'))
    is_paid = models.CharField(max_length=200, choices=NOYES, default='no', verbose_name=_('Is payment done?'))
    # General
    trade_code = models.CharField(max_length=20, null=True, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='pen', verbose_name=_('Status'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    @property
    def session_price(self):
        price = session_price_value
        return price

    @property
    def tax(self):
        tax = int(session_price_value * 0.1)
        return tax

    @property
    def session_price_plus_tax(self):
        price = int(session_price_value + session_price_value * 0.1)
        return price

    @property
    def commission(self):
        return self.commission

    def save(self, *args, **kwargs):
        if not self.trade_code:
            self.trade_code = generate_unique_id()
        super(TradeSession, self).save(*args, **kwargs)

    # @property
    # def tracking_code(self):
    #     number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #     choice_list = list(string.ascii_lowercase) + number_list + number_list
    #     code = ''
    #     for i in range(19):
    #         code = code + random.choice(choice_list)
    #     return code

    def get_absolute_url(self):
        return reverse('trade_detail', args=[self.id])



