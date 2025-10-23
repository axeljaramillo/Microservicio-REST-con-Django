from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    UsuariosViewSet,
    CursoViewSet,
    LeccionViewSet,
    InscripcionViewSet,
    ComentarioViewSet,
    health,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'usuarios', UsuariosViewSet, basename='usuarios')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'lecciones', LeccionViewSet, basename='leccion')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')
router.register(r'comentarios', ComentarioViewSet, basename='comentario')

urlpatterns = [
    path('', include(router.urls)),
    path('healthz/', health, name='healthz'),
]