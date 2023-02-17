from django.contrib import admin
from django.utils.html import format_html

from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    """User admin panel display fields"""
    list_display = ['id', 'email', 'name', 'photo_pre']
    readonly_fields = ('photo_pre',)

    def photo_pre(self, obj):
        """ image view in admin panel"""
        return format_html(f'<img style="height:100px;" src="/media/{obj.profile_picture}"/>')


admin.site.register(User, UserAdmin)
