import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.conf import settings
from django_quill.fields import QuillField


def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def generate_unique_code():
    return ''.join(random.choices(string.digits + string.digits, k=6))


class Case(models.Model):
    CASE_STATUSES = [
        ('a', _('Active')),
        ('s', _('Soon')),
        ('e', _('Ended')),
    ]
    title = models.CharField(max_length=300, verbose_name=_('Title'))
    maker = models.CharField(max_length=100, verbose_name=_('Maker'))
    province = models.CharField(max_length=50, verbose_name=_('Province'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    district = models.CharField(max_length=50, verbose_name=_('District'))
    capacity = models.PositiveIntegerField(blank=True, verbose_name=_('Capacity'))
    metric_price = models.PositiveIntegerField(verbose_name=_('Metric Price'))
    buy_assurance = models.BooleanField(default=False, verbose_name=_('Buy assurance'))
    guaranteed_gain = models.BooleanField(default=False, verbose_name=_('Guaranteed gain'))
    guaranteed_gain_percent = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Guaranteed gain percent'))
    end_time = models.CharField(max_length=200, verbose_name=_('End time'))
    description = QuillField(verbose_name=_('Description'))
    status = models.CharField(max_length=10, choices=CASE_STATUSES, verbose_name=_('Status'))
    cover = models.ImageField(upload_to='cases/covers/', blank=True, verbose_name=_('Case Cover'))
    cover2 = models.ImageField(upload_to='cases/covers/', null=True, blank=True, verbose_name=_('Case cover 2'))
    cover3 = models.ImageField(upload_to='cases/covers/', null=True, blank=True, verbose_name=_('Case cover 3'))
    cover4 = models.ImageField(upload_to='cases/covers/', null=True, blank=True, verbose_name=_('Case cover 4'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)
    unique_url_id = models.CharField(max_length=20, null=True, unique=True, blank=True)
    code = models.CharField(max_length=6, null=True, unique=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_url_id:
            self.unique_url_id = generate_unique_id()
        if not self.code:
            self.code = generate_unique_code()
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Case, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self):
        return f'{self.title} ""/"" {self.maker}'

    def get_absolute_url(self):
        return reverse('case_detail', args=[self.slug, self.unique_url_id])


class CaseOrder(models.Model):
    ORDER_STATUSES = [
        ('wa', _('Waiting')),
        ('ca', _('Canceled')),
        ('do', _('Done')),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    is_paid = models.BooleanField(default=False, verbose_name=_('Payment Status'))
    status = models.CharField(max_length=10, choices=ORDER_STATUSES, verbose_name=_('Status'))
    notes = models.CharField(max_length=1000, verbose_name=_('Notes'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date & time of creation'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date & time of modification'))

    def get_total_price(self):
        return sum(item.meter*item.price for item in self.item.all())

    def __str__(self):
        return f'Order: {self.id}'


class CaseOrderItem(models.Model):
    order = models.ForeignKey(CaseOrder, on_delete=models.CASCADE, related_name='item', verbose_name=_('Case Order'))
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Project'))
    meter = models.PositiveIntegerField(default=1, verbose_name=_('Area'))

    def __str__(self):
        return f'Order Item {self.id}: {self.case}x{self.meter}'



