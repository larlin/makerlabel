from django.contrib import admin

from .models import Tag

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User data',               {'fields': ['user_id', 'name']}),
        ('Box data', {'fields': ['box_number', 'comment']}),
    ]
    list_display = ('name', 'box_number')

admin.site.register(Tag, TagAdmin)
