import random
import string

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext as _

from .managers import CustomUserManager
from services.models import Counseling, Session, Visit
from restates.models import TradeSession

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


# --------------------------------- User ---------------------------------
class CustomUserModel(AbstractUser):
    IS_VERIFIED_CHOICES = [
        ('a', _('Authenticated')),
        ('n', _('Not Authenticated')),
        ('i', _('In Progress')),
    ]
    IS_AGENT_CHOICES = [
        ('is', _('Is')),
        ('wt', _('Waiting')),
        ('nt', _("Isn't")),
    ]
    AGENT_INFO_CHOICES = [
        ('cmp', _('Completed')),
        ('dnt', _('Not Completed')),
        ('ipr', _('In Progress')),
    ]
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    otp_code = models.PositiveIntegerField(blank=True, null=True)
    otp_code_datetime_created = models.DateTimeField(auto_now=True)
    is_verified = models.CharField(max_length=10, choices=IS_VERIFIED_CHOICES, blank=True, null=True, default='n', verbose_name=_('Authentication Status'))
    is_agent = models.CharField(max_length=10, choices=IS_AGENT_CHOICES, blank=True, null=True, default='nt', verbose_name=_('Is Agent?'))
    agent_info = models.CharField(max_length=10, choices=AGENT_INFO_CHOICES, blank=True, null=True, default='dnt', verbose_name=_('Complete Information'))

    objects = CustomUserManager()
    backend = 'accounts.backends.CustomAuthBackend'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    # Choices
    SEX_CHOICES = [
        ('m', _('Male')),
        ('f', _('Female')),
    ]
    INT_CHOICES = [
        ('ins', _('Instagram')),
        ('y&a', _('Course Videos')),
        ('ads', _('Advertisements')),
        ('web', _('Website and Google')),
        ('frd', _('Friends')),
        ('oth', _('Others')),
    ]
    EXP_CHOICES = [
        ('0', _('No Experience')),
        ('1', _('1 year')),
        ('2', _('2 years')),
        ('3', _('3 years')),
        ('4', _('4 years')),
        ('4', _('4 years')),
        ('5-10', _('5-10 years')),
        ('abv10', _('More than 10 years')),
    ]
    CRS_CHOICES = [
        ('have', _('Have')),
        ('dont', _('Have not')),
        ('seen', _('Have seen')),
    ]
    # Fields
    f_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('First Name'))
    l_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('Last Name'))
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True, verbose_name=_('Sex'))
    national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('National Code'))
    email = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('Email'))
    national_card = models.ImageField(upload_to='profile/images/auth/national_card/', blank=True, null=True, verbose_name=_('National Card Image'))
    auth_picture = models.ImageField(upload_to='profile/images/auth/auth_picture/', blank=True, null=True, verbose_name=_('Authentication Image'))
    bank_card = models.ImageField(upload_to='profile/images/auth/bank_card/', blank=True, null=True, verbose_name=_('Bank Card Image'))
    bank_sheba = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Bank Sheba'))
    province = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Province'))
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('City'))
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Postal Code'))
    address = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('Address'))
    introduction_way = models.CharField(max_length=10, choices=INT_CHOICES, blank=True, null=True, verbose_name=_('Introduction Way'))
    experience = models.CharField(max_length=10, choices=EXP_CHOICES, blank=True, null=True, verbose_name=_('Experience'))
    course_tendency = models.CharField(max_length=10, choices=CRS_CHOICES, blank=True, null=True, verbose_name=_('Course Tendency'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)


# --------------------------------- Tasks ---------------------------------
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def generate_unique_code():
    return ''.join(random.choices(string.digits + string.digits, k=6))


class Task(models.Model):
    TYPE_CHOICES = [
        ('cns', _('Counseling')),
        ('ses', _('Session')),
        ('vis', _('Visit')),
        ('tds', _('Trade Session')),
    ]
    PAYMENT_CHOICES = [
        ('yes', _('Yes')),
        ('no', _('No')),
    ]
    REQUEST_CHOICES = [
        ('tkn', _('Taken')),
        ('fre', _('Free')),
        ('pen', _('Pending')),
    ]
    task_trade_session = models.ForeignKey(TradeSession, on_delete=models.CASCADE, related_name='trade_session_task', blank=True, null=True)
    task_counseling = models.ForeignKey(Counseling, on_delete=models.CASCADE, related_name='counseling_task', blank=True, null=True)
    task_session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_task', blank=True, null=True)
    task_visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='visit_task', blank=True, null=True)
    agent = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='trade_session_agent', blank=True, null=True)
    is_paid = models.CharField(max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True, default='no', verbose_name=_('Payment Status'))
    is_commissioned = models.CharField(max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True, default='no', verbose_name=_('Commission Status'))
    is_requested = models.CharField(max_length=10, choices=REQUEST_CHOICES, blank=True, null=True, default='fre', verbose_name=_('Request Status'))
    unique_url_id = models.CharField(max_length=20, null=True, unique=True, blank=True)
    code = models.CharField(max_length=6, null=True, unique=True, blank=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, null=True, blank=True, verbose_name=_('Task Type'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    def save(self, *args, **kwargs):
        if not self.unique_url_id:
            self.unique_url_id = generate_unique_id()
        if not self.code:
            self.code = generate_unique_code()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.code} / {self.unique_url_id}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('agent_task_detail', args=[self.pk, self.unique_url_id])




