from django.contrib import admin

from .models import Subscribers

@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    pass