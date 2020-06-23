from django.contrib import admin
from .models import FileModel, UserProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(FileModel)
