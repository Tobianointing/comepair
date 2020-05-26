from django.contrib import admin


from .models import Thread, ChatMessage, Notification

admin.site.register(ChatMessage)

class ChatMessage1(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage1]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Notification)

