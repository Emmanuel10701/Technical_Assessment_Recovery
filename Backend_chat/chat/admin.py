from django.contrib import admin
from .models import User, Chat

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'tokens')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response', 'timestamp')
    list_filter = ('user', 'timestamp')
