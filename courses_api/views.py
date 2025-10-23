from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import curso, usuarios, lecciones, comentarios, inscripciones
from .serializers import (
    UserSerializer,
    UsuariosSerializer,
    CursoSerializer,
    LeccionSerializer,
    ComentarioSerializer,
    InscripcionSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']


class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = usuarios.objects.select_related('user').all()
    serializer_class = UsuariosSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido', 'email', 'telefono']


class CursoViewSet(viewsets.ModelViewSet):
    queryset = curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'rol']
    search_fields = ['nombre', 'categoria']
    ordering_fields = ['created_at', 'nombre']


class LeccionViewSet(viewsets.ModelViewSet):
    queryset = lecciones.objects.select_related('curso').all()
    serializer_class = LeccionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['curso']
    search_fields = ['titulo']
    ordering_fields = ['fecha_creacion', 'created_at']


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = inscripciones.objects.select_related('usuario', 'curso').all()
    serializer_class = InscripcionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['usuario', 'curso', 'activa']
    search_fields = ['curso__nombre', 'usuario__nombre']
    ordering_fields = ['fecha_inscripcion', 'created_at']


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = comentarios.objects.select_related('usuario', 'leccion').all()
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['leccion', 'usuario']
    search_fields = ['contenido', 'leccion__titulo', 'usuario__nombre']
    ordering_fields = ['fecha_creacion', 'created_at']


def health(request):
    return JsonResponse({
        "status": "ok",
        "app": "courses_api"
    })
