from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(CorrectAnswer)
admin.site.register(WrongAnswer)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserProfile)
