from django.contrib import admin
from .models import Message, UserChannel

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_who', 'to_who', 'date', 'time', 'has_been_seen')
    list_filter = ('from_who', 'to_who', 'date', 'has_been_seen')
    search_fields = ('from_who__username', 'to_who__username', 'message')

@admin.register(UserChannel)
class UserChannelAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel_name')
    list_filter = ('user',)
    search_fields = ('user__username', 'channel_name')