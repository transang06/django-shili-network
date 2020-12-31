from django.contrib import admin
from user.models import *

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Follower)
admin.site.register(Conversation)
admin.site.register(Message)
