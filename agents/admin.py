from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AgentCustomUserModel, AgentProfile, Province, City
from . import forms


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    model = AgentProfile
    list_display = ('agent', 'f_name', 'l_name', 'sex', 'national_code', 'email', 'fixed_phone_number', 'province', 'city',
                  'postal_code', 'address', 'national_card', 'auth_picture', 'bank_card', 'bank_sheba', 'experience',
                  'course_tendency', 'introduction_way',)


class AgentProfileInline(admin.StackedInline):
    model = AgentProfile
    can_delete = False
    verbose_name_plural = 'agent_profiles'
    fields = ('agent', 'f_name', 'l_name', 'sex', 'national_code', 'email', 'fixed_phone_number', 'province', 'city',
              'postal_code', 'address', 'national_card', 'auth_picture', 'bank_card', 'bank_sheba', 'experience',
              'course_tendency', 'introduction_way',)


class AgentCustomUserAdmin(BaseUserAdmin):
    form = forms.AgentAdminPanelUserChangeForm
    add_form = forms.AgentAdminPanelUserCreateForm
    inlines = (AgentProfileInline, )

    list_display = ('phone_number', 'complete_info', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'complete_info')}),
        # ('Personal info', {'fields': ('profile', 'complete_info')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.register(AgentCustomUserModel, AgentCustomUserAdmin)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')

