from django.contrib import admin
from .models import *
# Register your models here.

#admin.site.register(Member)

admin.site.register(UploadFileModel)
admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(Notice)
admin.site.register(TR)
admin.site.register(Member)
admin.site.register(Notification)
admin.site.register(Calendar)
admin.site.register(Participate)

def __str__(self) :
      return self.title
'''
def __str__(self) :
      return self.name
'''