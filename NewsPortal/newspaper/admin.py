from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import *

User = get_user_model()

admin.site.register(Post)
admin.site.register(Category)

admin.site.register(User, UserAdmin)

