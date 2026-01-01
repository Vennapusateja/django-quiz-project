
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.html import format_html
from .models import Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'grade')
    search_fields = ('text',)
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    inlines = [QuestionInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_choice', 'is_correct', 'submitted_at')
    list_filter = ('is_correct',)
    search_fields = ('user__username', 'question__text')


admin.site.register(User, UserAdmin)
