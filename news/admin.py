from django.contrib import admin
from news.models import NewsEntry


class NewsEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'is_published', 'summary')
    list_filter = ('timestamp', 'is_published')
    ordering = ('-timestamp', )
    # readonly_fields = ('user',)


admin.site.register(NewsEntry, NewsEntryAdmin)