from django.contrib import admin
from .models import User, Chat

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'tokens', 'date_joined')
    search_fields = ('username',)
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message_preview', 'response_preview', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'message', 'response')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

    def response_preview(self, obj):
        return obj.response[:50] + '...' if len(obj.response) > 50 else obj.response
    response_preview.short_description = 'Response'
