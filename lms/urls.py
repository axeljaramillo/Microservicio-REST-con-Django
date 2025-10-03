from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
router.register(r'reviews', views.CourseReviewViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),

]
