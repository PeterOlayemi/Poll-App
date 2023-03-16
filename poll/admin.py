from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = 'WesterGren Admin'
admin.site.site_title = 'WesterGren Admin Panel'
admin.site.index_title = 'WesterGren Admin Panel'

class OptionInLine(admin.TabularInline):
    model = Option
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['question']}), ('Date Information', {'fields':['date'], 'classes':['collapse']})]
    inlines = [OptionInLine]
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote)
