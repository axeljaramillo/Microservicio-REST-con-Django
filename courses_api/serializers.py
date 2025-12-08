from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Sum, Avg
from .models import Course, Lesson, Enrollment, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']
        ref_name = 'CoursesApiUser'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CourseSerializer(serializers.ModelSerializer):
    # Set instructor automatically from the current user on write. HiddenField will populate the value
    # using CurrentUserDefault() without requiring clients to send it.
    instructor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    instructor_username = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'instructor_username', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'instructor_username', 'instructor']
        ref_name = 'CoursesApiCourse'


class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'course_title', 'title', 'content', 'order', 'duration_minutes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'course_title']
        ref_name = 'CoursesApiLesson'


class EnrollmentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'user_username', 'course', 'course_title', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_username', 'course_title']
        ref_name = 'CoursesApiEnrollment'


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_username', 'course', 'course_title', 'content', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_username', 'course_title']
        ref_name = 'CoursesApiComment'


class CourseDetailSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    enrollments_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'is_published',
            'created_at', 'updated_at', 'lessons', 'lesson_count', 'total_duration',
            'enrollments_count', 'average_rating'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        ref_name = 'CoursesApiCourseDetail'

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_total_duration(self, obj):
        return obj.lessons.aggregate(total=Sum('duration_minutes'))['total'] or 0

    def get_enrollments_count(self, obj):
        return obj.enrollments.count()

    def get_average_rating(self, obj):
        from django.db.models import Avg
        avg = obj.comments.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 2) if avg is not None else None
