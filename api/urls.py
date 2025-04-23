from django.urls import path
from .views import (
    category_list, course_list, course_detail,
    EnrollView, MyCoursesView, LogoutView,
    short_course_list, user_list, LessonDetailView,
    register_user  # 👈 добавили
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('categories/', category_list),
    path('courses/', course_list),
    path('courses/<int:pk>/', course_detail),
    path('courses/short/', short_course_list),
    path('users/', user_list),

    path('enroll/', EnrollView.as_view()),
    path('my-courses/', MyCoursesView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('lessons/<int:lesson_id>/', LessonDetailView.as_view()),
    path('register/', register_user),  # 👈 добавили

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
