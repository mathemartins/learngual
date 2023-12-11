from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField('Participant', related_name='chat_rooms')

    class Meta:
        db_table = "chat_room"
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.CharField(max_length=100)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_by = models.ManyToManyField('Participant', related_name='read_messages', blank=True)

    def mark_as_read(self, user):
        self.is_read = True
        self.save()

    class Meta:
        db_table = "message"
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f'{self.user}: {self.content[:50]}...'
