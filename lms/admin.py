from django.contrib import admin

# Register your models here.
from .models import Profile, Category, Course, Lesson, Enrollment, LessonProgress, CourseReview

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(CourseReview)
