from django.contrib import admin

from chat.models import ChatRoom, Message, Participant


# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(Participant)
admin.site.register(Message)

# @admin.register(ChatRoom)
# class ChatRoomModelAdmin(admin.ModelAdmin):
#     list_filter = ('participants',)
#     list_display = ('name',)
#     search_fields = ('name',)
#
#
# @admin.register(Message)
# class MessageModelAdmin(admin.ModelAdmin):
#     list_display = ('user', 'room', 'content', 'timestamp', 'is_read',)
#     list_editable = ('content',)
#     search_fields = ('content', 'room',)
