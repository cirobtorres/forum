from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Account


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name = 'Account'
    verbose_name_plurals = 'Accounts'


class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = 'id', 'user', 'gender', 'city', 'state', 
    list_display = 'user', 'birth_date', 'gender', 'city', 'state', 'img', 
    list_display_links = 'user', 
    list_filter = 'gender', 'state', 