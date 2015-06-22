from django.contrib import admin

from .models import Tag

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User data',               {'fields': ['user_id', 'name']}),
        ('Box data', {'fields': ['box_number', 'comment', 'visible']}),
    ]
    list_display = ('name', 'box_number', 'visible')

admin.site.register(Tag, TagAdmin)
