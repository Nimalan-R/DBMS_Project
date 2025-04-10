from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("age", "is_student")}),
    )
    list_display = ("username", "email", "is_student", "age", "is_staff")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "total_questions", "created_at")
    list_filter = ("subject",)
    search_fields = ("title",)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz")
    list_filter = ("quiz", "tags")
    search_fields = ("text",)
    inlines = [AnswerInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)


class ResultDetailInline(admin.TabularInline):
    model = ResultDetail
    extra = 0


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "timestamp")
    list_filter = ("quiz", "timestamp")
    inlines = [ResultDetailInline]


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user", "total_quizzes_taken", "total_score", "average_score", "total_time_seconds", "last_updated"
    )
    readonly_fields = ("last_updated",)
    search_fields = ("user__username",)
