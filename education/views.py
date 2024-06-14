from .serializers import *
from .models import *
from .utils import send_email
from rest_framework import viewsets, filters, status, permissions, generics, views
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserRegisterApi(viewsets.ModelViewSet):
    '''
    Registratsiya uchun api
    '''
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'username', 'email', 'fist_name', 'last_name']


class UserLoginApi(views.APIView):
    '''
    Login uchun api
    '''
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        return Response({
            'success': 'User logged in successfully.',
            'username': validated_data['username'],
            'tokens': validated_data['tokens'],
        }, status=status.HTTP_200_OK)


class UserProfileApi(viewsets.ModelViewSet):
    '''
    Profil uchun api
    bundan foydalanish uchun Autenfikatsiyadan otgan bolishi kerak
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'user', 'full_name', 'telegram']


class StatusApi(viewsets.ModelViewSet):
    '''
    Status uchun
    '''
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'name']


class TeacherApi(viewsets.ModelViewSet):
    '''
    Teacher uchun
    '''
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    filterset_fields = ['status']
    search_fields = ['id', 'user', 'full_name']

class ModeratorApi(TeacherApi):
    '''
    Moderator uchun
    '''
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer


class CategoryApi(viewsets.ModelViewSet):
    '''
    Kategoriya uchun api
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'name']



class CourseApi(viewsets.ModelViewSet):
    '''
    Kurs uchun api
    '''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    filterset_fields = ['category']
    search_fields = ['id', 'name', 'category', 'description']

class LessonApi(viewsets.ModelViewSet):
    '''
    Dars uchun api
    '''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    search_fields = ['id', 'title', 'course']
    filterset_fields = ['course']



class LessonVideoApi(viewsets.ModelViewSet):
    '''
    Dars videosi uchun
    '''
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    filterset_fields = ['lesson']
    search_fields = ['id', 'name', 'lesson', 'video']

class LessonHomeworkApi(viewsets.ModelViewSet):
    '''
    Dars uyga vazifasi uchun
    '''
    queryset = LessonHomework.objects.all()
    serializer_class = LessonHomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['lesson_video']
    search_fields = ['id', 'homework', 'file', 'lesson_video']



class HomeworkFromStudentsApi(viewsets.ModelViewSet):
    '''
    Oquvchilar uyga vazifani yuklashi uchun api
    '''
    queryset = HomeworkFromStudent.objects.all()
    serializer_class = HomeworkFromStudentSerialzier
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['lesson_homework']
    search_fields = ['id', 'student', 'lesson_homework', 'file']

class RatingApi(viewsets.ModelViewSet):
    '''
    Lesson Videolarga reyting berish uchun
    '''
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['lesson_video', 'user', 'score']
    search_fields = ['id', 'lesson_video', 'user', 'score']


class CommentApi(viewsets.ModelViewSet):
    '''
    Darslarga izoh qoshish uchun
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SendEmailApi(views.APIView):
    '''
    Barcha foydalanuvchilarning emailigi xabar yuborish
    '''
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        users = User.objects.all()
        subject = request.data.get('subject')
        message = request.data.get('message')
        template_name = 'email_from_admin.html'

        for user in users:
            send_email(
                user=user,
                subject=subject,
                template_name=template_name,
                context={'message': message, 'user': user, 'subject': subject, }
            )

        return Response({'success': 'Email jonatildi'})

