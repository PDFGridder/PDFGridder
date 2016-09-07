from django.contrib import admin
from .models import Grid

class AdminGrid(admin.ModelAdmin):
    list_display = ('paper','margins','columns','columns_gutter_str','baseline_str','created','user','name')
    list_filter = ('created','user')
admin.site.register(Grid, AdminGrid)
