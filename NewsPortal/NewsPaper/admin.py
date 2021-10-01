from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post, Category, CustomUser

admin.site.register(Post)
admin.site.register(Category)

admin.site.register(CustomUser)