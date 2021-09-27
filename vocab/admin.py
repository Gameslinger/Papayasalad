from django.contrib import admin
from .models import *

class VocabWordInline(admin.StackedInline):
	model = VocabWord
class VocabListAdmin(admin.ModelAdmin):
	inlines = [VocabWordInline]
	
admin.site.register(VocabList, VocabListAdmin)