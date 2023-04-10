from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
# Register your models here.


# NOTE5: customising the default useradmin
# Import useradmina s baseuseradmin
# and add ordering and list display
# then register and specify to use the custom UserAdmin we created
# fieldsets will enable editing the users in the admin page, give the heading and fields to display
# add the readonly values
# add the add_fieldsets to enable adding users
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'), {
                'fields': ('is_staff', 'is_active', 'is_superuser')}
        ),
        # the , is important cuz it should be a tuple
        (_('Important dates'), {'fields': ('last_login',)})


    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # this is to add css class
            'fields': ('email', 'password1', 'password2', 'name', 'is_active', 'is_staff', 'is_superuser',)
        }),  # NOTE:ERROR: TypeError at /admin/core/user/add/cannot unpack non-iterable NoneType object if you miss this coma cuz it wont be tuple else
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)  # no custom manager here
