from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class curso(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    rol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} - {self.id} - {self.categoria} - {self.rol}"


class usuarios(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='courses_api_perfil')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.id} - {self.email} - {self.rol}"


class lecciones(TimeStampedModel):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    curso = models.ForeignKey(curso, on_delete=models.CASCADE, related_name='lecciones')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.titulo} - {self.id} - {self.curso.nombre}"


class comentarios(TimeStampedModel):
    usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name='comentarios')
    leccion = models.ForeignKey(lecciones, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comentario {self.id} by {self.usuario.nombre} on {self.leccion.titulo}"


class inscripciones(TimeStampedModel):
    usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f"{self.usuario.nombre} inscrito en {self.curso.nombre} ({'activa' if self.activa else 'inactiva'})"