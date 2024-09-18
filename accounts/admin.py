from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUserModel, Profile
from .forms import AdminPanelUserCreateForm, AdminPanelUserChangeForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'f_name', 'l_name', 'national_code', 'email', 'national_card', 'auth_picture',
                    'bank_card', 'bank_sheba', 'province', 'city')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('user', 'f_name', 'l_name', 'national_code', 'email', 'national_card', 'auth_picture',
              'bank_card', 'bank_sheba', 'province', 'city')


class CustomUserAdmin(BaseUserAdmin):
    form = AdminPanelUserChangeForm
    add_form = AdminPanelUserCreateForm
    inlines = (ProfileInline, )

    list_display = ('phone_number', 'is_agent', 'is_verified', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'is_verified', 'is_agent')}),
        # ('Personal info', {'fields': ('profile', 'is_verified')}),
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


admin.site.register(CustomUserModel, CustomUserAdmin)



