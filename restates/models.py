import random
import string

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext as _

from . import statuses


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


# --------------------------------- File ---------------------------------
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

class SaleFile(models.Model):
    # location fields
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='files', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='files', verbose_name=_('City'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='files', verbose_name=_('District'))
    # general characteristics
    price = models.PositiveBigIntegerField(verbose_name=_('Price'))
    room = models.CharField(max_length=15, choices=statuses.rooms, verbose_name=_('Number of Rooms'))
    area = models.PositiveIntegerField(verbose_name=_('Area'))
    year = models.CharField(max_length=15, choices=statuses.years, verbose_name=_('Year of Construction'))
    document = models.CharField(max_length=15, choices=statuses.booleans, verbose_name=_('Document'))
    level = models.CharField(max_length=15, choices=statuses.levels, verbose_name=_('Level'))
    parking = models.CharField(max_length=15, choices=statuses.booleans, verbose_name=_('Parking'))
    elevator = models.CharField(max_length=15, choices=statuses.booleans, verbose_name=_('Elevator'))
    warehouse = models.CharField(max_length=15, choices=statuses.booleans, verbose_name=_('Warehouse'))
    cover = models.ImageField(upload_to='files/covers/', blank=True, verbose_name=_('File cover'))
    cover2 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 2'))
    cover3 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 3'))
    cover4 = models.ImageField(upload_to='files/covers/', null=True, blank=True, verbose_name=_('File cover 4'))
    # optional
    direction = models.CharField(max_length=15, choices=statuses.directions, null=True, blank=True, verbose_name=_('File Direction'))
    file_levels = models.CharField(max_length=15, choices=statuses.levels, null=True, blank=True, verbose_name=_('File Levels Number'))
    aparts_per_level = models.CharField(max_length=15, choices=statuses.aparts_per_level, null=True, blank=True, verbose_name=_('Apartments per Level'))
    restoration = models.CharField(max_length=15, choices=statuses.restorations, null=True, blank=True, verbose_name=_('Restoration'))
    bench_stove = models.CharField(max_length=15, choices=statuses.booleans, null=True, blank=True, verbose_name=_('Bench Stove'))
    balcony = models.CharField(max_length=15, choices=statuses.booleans, null=True, blank=True, verbose_name=_('Balcony'))
    toilet = models.CharField(max_length=15, choices=statuses.toilets, null=True, blank=True, verbose_name=_('Toilet'))
    hot_water = models.CharField(max_length=15, choices=statuses.hot_water, null=True, blank=True, verbose_name=_('Hot Water System'))
    cooling = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Cooling System'))
    heating = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Heating System'))
    floor = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('Floor Type'))
    # general information
    title = models.CharField(max_length=230, verbose_name=_('File Title'))
    description = models.TextField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True, allow_unicode=True)
    unique_url_id = models.CharField(max_length=20, null=True, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=statuses.statuses, default='pen')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_expired = models.DateTimeField(blank=True, null=True)
    # personal information
    provider_name = models.CharField(max_length=50, verbose_name=_('Provider Name'))
    phone_number_for_contact = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Provider Phone Number'))
    provider_national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Provider National Code'))
    owner_national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Owner National Code'))
    file_postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('File Postal Code'))

    # @property
    # def tracking_code(self):
    # 	number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # 	choice_list = list(string.ascii_lowercase) + number_list + number_list
    # 	code = ''
    # 	for i in range(19):
    # 		code = code + random.choice(choice_list)
    # 	return code

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
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(SaleFile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} / {self.unique_url_id}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('file_detail', args=[self.slug, self.unique_url_id])

