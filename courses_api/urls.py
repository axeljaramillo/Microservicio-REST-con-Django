from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CourseViewSet,
    LessonViewSet,
    EnrollmentViewSet,
    CommentViewSet,
)

router = DefaultRouter()
# English endpoints
router.register(r'users', UserViewSet, basename='user')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'comments', CommentViewSet, basename='comment')

# Spanish aliases to avoid 404 when using Spanish paths
router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'cursos', CourseViewSet, basename='cursos')
router.register(r'lecciones', LessonViewSet, basename='lecciones')
router.register(r'inscripciones', EnrollmentViewSet, basename='inscripciones')
router.register(r'comentarios', CommentViewSet, basename='comentarios')

urlpatterns = [
    path('', include(router.urls)),
]