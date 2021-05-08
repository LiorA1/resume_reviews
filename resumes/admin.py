from django.contrib import admin

# Register your models here.

from .models import Resume, Review

admin.site.register(Resume)
admin.site.register(Review)
