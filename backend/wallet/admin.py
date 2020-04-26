from django.contrib import admin
from .models import Wallet
# Register your models here.


class AdminWallet(admin.ModelAdmin):
    list_display = ['user', 'description']
    list_filter = ['user']


admin.site.register(Wallet,AdminWallet)