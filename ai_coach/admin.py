from django.contrib import admin
from .models import CoachingSession

@admin.register(CoachingSession)
class CoachingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'question_preview')
    list_filter = ('user', 'created_at')
    search_fields = ('question', 'response')
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'
