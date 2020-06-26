from django.contrib import admin
from .models import Tag


class TagsAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.name


admin.site.register(Tag, TagsAdmin)