from django.contrib import admin
from .models import curso, usuarios, lecciones, comentarios, inscripciones

@admin.register(curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "rol", "created_at")
    list_filter = ("categoria", "rol")
    search_fields = ("nombre", "categoria")


@admin.register(usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "nombre", "apellido", "email", "rol", "created_at")
    list_filter = ("rol",)
    search_fields = ("nombre", "apellido", "email", "user__username")


@admin.register(lecciones)
class LeccionesAdmin(admin.ModelAdmin):
    list_display = ("id", "curso", "titulo", "fecha_creacion")
    list_filter = ("curso",)
    search_fields = ("titulo", "curso__nombre")


@admin.register(inscripciones)
class InscripcionesAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "curso", "activa", "fecha_inscripcion")
    list_filter = ("activa", "curso")
    search_fields = ("usuario__nombre", "curso__nombre")


@admin.register(comentarios)
class ComentariosAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "leccion", "fecha_creacion")
    list_filter = ("leccion",)
    search_fields = ("contenido", "usuario__nombre", "leccion__titulo")
