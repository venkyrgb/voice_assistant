from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(voice_history)
class voice_historyAdmin(admin.ModelAdmin):
    list_display = ('user', 'voice_text', 'voice_date')
    list_filter = ('user',)
    ordering = ('-voice_date',)
