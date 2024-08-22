from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _

from .managers import AgentCustomUserManager
from accounts.models import CustomUserModel


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


# --------------------------------- Models ---------------------------------
class AgentCustomUserModel(AbstractUser):
    # pass
    COMPLETE_INFO_CHOICES = [
        ('cmp', _('Completed')),
        ('dnt', _('Not Completed')),
        ('ipr', _('In Progress')),
    ]
    username = None
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('Phone Number'))
    otp_code = models.PositiveIntegerField(blank=True, null=True)
    otp_code_datetime_created = models.DateTimeField(auto_now=True)
    complete_info = models.CharField(max_length=10, choices=COMPLETE_INFO_CHOICES, blank=True, null=True, default='n', verbose_name=_('Complete Information'))

    objects = AgentCustomUserManager()
    backend = 'agents.backends.AgentCustomAuthBackend'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name='agent_custom_users',  # Unique related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='agent_custom_user_permissions',  # Unique related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class AgentProfile(models.Model):
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
    national_code = models.CharField(max_length=10, blank=True, null=True, unique=True, verbose_name=_('National Code'))
    fixed_phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Fixed Phone Number'))
    email = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('Email'))
    national_card = models.ImageField(upload_to='agents/national_card/', blank=True, null=True, verbose_name=_('National Card Image'))
    auth_picture = models.ImageField(upload_to='agents/auth_picture/', blank=True, null=True, verbose_name=_('Authentication Image'))
    bank_card = models.ImageField(upload_to='agents/bank_card/', blank=True, null=True, verbose_name=_('Bank Card Image'))
    bank_sheba = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Bank Sheba'))
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_files', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_files', verbose_name=_('City'))
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Postal Code'))
    address = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('Address'))
    agent = models.OneToOneField(AgentCustomUserModel, on_delete=models.CASCADE, related_name='agent_profile', blank=True, null=True)
    introduction_way = models.CharField(max_length=10, choices=INT_CHOICES, blank=True, null=True, verbose_name=_('Introduction Way'))
    experience = models.CharField(max_length=10, choices=EXP_CHOICES, blank=True, null=True, verbose_name=_('Experience'))
    course_tendency = models.CharField(max_length=10, choices=CRS_CHOICES, blank=True, null=True, verbose_name=_('Course Tendency'))

