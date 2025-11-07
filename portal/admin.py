from django.contrib import admin
from .models import Control, Risk

@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('control_id', 'title')
    search_fields = ('control_id', 'title')

@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('name',)
