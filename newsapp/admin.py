from django.contrib import admin
from newsapp.models import Contacts, News, Questions, Category, LiveNews, AboutSite
from django.forms import TextInput, Textarea
from django.db import models
# Register your models here.


class AboutSiteAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class NewsAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Contacts)
admin.site.register(AboutSite, AboutSiteAdmin)
admin.site.register(Questions)
admin.site.register(LiveNews)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
