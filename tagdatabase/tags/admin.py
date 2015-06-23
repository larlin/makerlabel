from django.contrib import admin

from .models import Tag
from .models import Member

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User data', {'fields': ['member_id', ]}),
        ('Box data', {'fields': ['box_number', 'comment', 'visible']}),
    ]
    list_display = ('box_number', 'visible')

class MemberAdmin(admin.ModelAdmin):
	list_display = ('name', 'box_num')

admin.site.register(Member, MemberAdmin)
admin.site.register(Tag, TagAdmin)
