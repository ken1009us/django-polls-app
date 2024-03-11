from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["publish_date"]}),
    ]

    inlines = [ChoiceInline]

    list_display = ["question_text", "publish_date", "was_published_recently"]
    list_filter = ["publish_date"]


admin.site.register(Question, QuestionAdmin)
