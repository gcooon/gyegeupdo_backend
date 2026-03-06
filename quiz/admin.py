from django.contrib import admin
from .models import QuizSession


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'user', 'category', 'budget_max', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['session_key', 'user__email']
    readonly_fields = ['session_key', 'created_at']
    raw_id_fields = ['user', 'category']
