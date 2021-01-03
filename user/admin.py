from django.contrib import admin
from user.models import *


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'content', 'created_at']


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Follower)
admin.site.register(Conversation)
admin.site.register(Message, MessageAdmin)
