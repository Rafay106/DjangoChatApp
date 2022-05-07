from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(TopicModel)
admin.site.register(UserModel)
admin.site.register(RoomModel)
admin.site.register(MessageModel)