from django.contrib import admin

from .models import News

class NewsAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'url',)

admin.site.register(News, NewsAdmin)