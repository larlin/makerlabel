from django.contrib import admin

from .models import MemberBoxTag
from .models import MemberShelfTag
from .models import Member
from .models import MachineTag
from .models import Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = "machine"

class MemberBoxTagAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User data', {'fields': ['member_id', ]}),
        ('Box data', {'fields': ['box_number', 'print_date',  'comment', 'visible']}),
    ]
    list_display = ('member_id', 'box_number', 'visible')
    

class MemberShelfTagAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'visible')

class MemberAdmin(admin.ModelAdmin):
	list_display = ('name', 'box_num')

class MachineTagAdmin(admin.ModelAdmin):
    list_display = ('contact', 'info')
    inlines = [
        CommentInline,
    ]
    


admin.site.register(Member, MemberAdmin)
admin.site.register(MemberBoxTag, MemberBoxTagAdmin)
admin.site.register(MemberShelfTag, MemberShelfTagAdmin)
admin.site.register(MachineTag, MachineTagAdmin)
