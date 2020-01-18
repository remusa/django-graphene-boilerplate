from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "id",
        "description",
        "url",
        "posted_by",
        "updated_at",
        "created_at",
    ]


admin.site.register(Link, LinkAdmin)
