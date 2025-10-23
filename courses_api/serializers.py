from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import curso, usuarios, lecciones, comentarios, inscripciones

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UsuariosSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = usuarios
        fields = ['id', 'user', 'user_username', 'nombre', 'apellido', 'email', 'telefono', 'rol', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_username']


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = curso
        fields = ['id', 'nombre', 'categoria', 'rol', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeccionSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)

    class Meta:
        model = lecciones
        fields = ['id', 'titulo', 'contenido', 'curso', 'curso_nombre', 'fecha_creacion', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'curso_nombre']


class ComentarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    leccion_titulo = serializers.CharField(source='leccion.titulo', read_only=True)

    class Meta:
        model = comentarios
        fields = ['id', 'usuario', 'usuario_nombre', 'leccion', 'leccion_titulo', 'contenido', 'fecha_creacion', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'usuario_nombre', 'leccion_titulo']


class InscripcionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)

    class Meta:
        model = inscripciones
        fields = ['id', 'usuario', 'usuario_nombre', 'curso', 'curso_nombre', 'fecha_inscripcion', 'activa', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'usuario_nombre', 'curso_nombre']
