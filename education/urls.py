from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('register', UserRegisterApi)
router.register('profile', UserProfileApi)
router.register('status', StatusApi)
router.register('teacher', TeacherApi)
router.register('moderator', ModeratorApi)
router.register('category', CategoryApi)
router.register('course/lesson/video/students-homework', HomeworkFromStudentsApi)
router.register('course/lesson/video/homework', LessonHomeworkApi)
router.register('course/lesson/video/rating', RatingApi)
router.register('course/lesson/video', LessonVideoApi)
router.register('course/lesson/comments', CommentApi, basename='comment')
router.register('course/lesson', LessonApi)
router.register('course', CourseApi, basename='course')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/login/', UserLoginApi.as_view()),
    path('api/v1/sent-email/', SendEmailApi.as_view())
]