from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .models import Category, Course, Enrollment, Lesson
from .serializers import (
    CourseSerializer,
    CategorySerializer,
    EnrollmentSerializer,
    CourseShortSerializer,
    UserPublicSerializer
)

# --- Выход из аккаунта ---
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы успешно вышли"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Неверный токен или уже заблокирован"}, status=status.HTTP_400_BAD_REQUEST)

# --- Список категорий ---
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# --- Детали курса (теперь с проверкой на запись) ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_detail(request, pk):
    try:
        course = Course.objects.select_related('category', 'author').prefetch_related('modules__lessons').get(id=pk)
    except Course.DoesNotExist:
        return Response({"detail": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

    is_enrolled = Enrollment.objects.filter(course=course, user=request.user).exists()
    serializer = CourseSerializer(course, context={
        'request': request,
        'is_enrolled': is_enrolled
    })
    return Response(serializer.data)

# --- Список всех курсов ---
@api_view(['GET'])
def course_list(request):
    courses = Course.objects.select_related('category', 'author').prefetch_related('modules__lessons')
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

# --- Краткий список курсов ---
@api_view(['GET'])
def short_course_list(request):
    courses = Course.objects.select_related('category', 'author')  # ← ЭТО обязательно!
    serializer = CourseShortSerializer(courses, many=True)
    return Response(serializer.data)


# --- Список пользователей ---
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserPublicSerializer(users, many=True)
    return Response(serializer.data)

# --- Регистрация ---
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=201)

# --- Запись на курс ---
class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course')
        if not course_id:
            return Response({'error': 'Не указан курс'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, записан ли уже пользователь
        already_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
        if already_enrolled:
            return Response({'message': 'Вы уже записаны на этот курс'}, status=status.HTTP_200_OK)

        # Если не записан — создаём запись
        Enrollment.objects.create(user=request.user, course=course)
        return Response({'message': 'Вы успешно записались на курс!'}, status=status.HTTP_201_CREATED)


# --- Мои курсы ---
class MyCoursesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course__category', 'course__author')
        courses = [e.course for e in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

# --- Доступ к уроку (если записан) ---
class LessonDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'detail': 'Урок не найден'}, status=status.HTTP_404_NOT_FOUND)

        course = lesson.module.course
        user = request.user

        if not Enrollment.objects.filter(user=user, course=course).exists():
            return Response({'detail': 'Вы не записаны на этот курс'}, status=status.HTTP_403_FORBIDDEN)

        return Response({
            'id': lesson.id,
            'title': lesson.title,
            'video_url': request.build_absolute_uri(lesson.video.url),
            'module': lesson.module.title,
            'order': lesson.order
        })
