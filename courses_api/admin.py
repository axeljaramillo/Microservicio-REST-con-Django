from django.contrib import admin
from .models import Course, Lesson, Enrollment, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "instructor", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description", "instructor__username")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "title", "order", "duration_minutes")
    list_filter = ("course",)
    search_fields = ("title", "course__title")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "is_active", "created_at")
    list_filter = ("is_active", "course")
    search_fields = ("user__username", "course__title")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "rating", "created_at")
    list_filter = ("rating", "course")
    search_fields = ("content", "user__username", "course__title")
