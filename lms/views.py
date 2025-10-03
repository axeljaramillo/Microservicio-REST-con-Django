from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

from .models import (
    Profile, Category, Course, Lesson, Enrollment,
    LessonProgress, CourseReview
)
from .serializers import (
    ProfileSerializer, CategorySerializer, CourseSerializer,
    LessonSerializer, EnrollmentSerializer, LessonProgressSerializer, CourseReviewSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Profile model"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_instructor']
    search_fields = ['user__username', 'bio']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Category model (read-only)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course model"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['difficulty', 'status', 'category', 'instructor']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'price']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson model"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'lesson_type', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title', 'created_at']
    ordering = ['course', 'order']


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment model"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'course', 'student']
    search_fields = ['course__title']
    ordering_fields = ['enrolled_at']
    ordering = ['-enrolled_at']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class CourseReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for CourseReview model"""
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'rating']
    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class LessonProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for LessonProgress model"""
    queryset = LessonProgress.objects.all()
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'lesson', 'is_completed']
    search_fields = ['lesson__title']
    ordering_fields = ['completed_at', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
