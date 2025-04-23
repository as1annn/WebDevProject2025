from rest_framework import serializers
from .models import Category, Course, Module, Lesson, Enrollment
from django.contrib.auth.models import User

# --- ModelSerializers ---

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_video_url(self, obj):
        request = self.context.get('request')
        is_enrolled = self.context.get('is_enrolled', False)
        if obj.video and request and is_enrolled:
            return request.build_absolute_uri(obj.video.url)
        return None  # 👈 Если не записан — не отдаём ссылку
        

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'author', 'preview_video', 'modules']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


# --- Serializer (ручные) ---

class CourseShortSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'author']



class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
