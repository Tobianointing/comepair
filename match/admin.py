from django.contrib import admin

# Register your models here.
from .models import (
	Answer, User_Answer, Question,
	Choice
	)

admin.site.register(Answer)
admin.site.register(User_Answer)
admin.site.register(Question)
admin.site.register(Choice)

