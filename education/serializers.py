from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .validators import validate_password, validate_email

class EmailSerializer(serializers.Serializer):
    '''
    emailga xabar yuborish uchun
    '''
    subject = serializers.CharField(max_length=255, required=True, write_only=True)
    message = serializers.CharField(required=True, write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Bu profil modeli uchun serializer
    '''
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'photo', 'address', 'phone_number', 'telegram']


class UserRegisterSerializer(serializers.ModelSerializer):
    '''
    Bu registratsiya uchun serializer
    '''
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'},)
    password2 = serializers.CharField(write_only=True, required=True,validators=[validate_password], style={'input_type': 'password'}, label="Parolni tasdiqlang")

    class Meta:
        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')


    def validate(self, data):
        '''
        Parollarni moslikga tekshiradi,
        mos bomasa xatolik beradi
        '''
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Parol mos kelmadi!!!")
        return data

    def create(self, validated_data):
        '''
        Yangi user yaratadi
        '''
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    '''
    Login uchun serializer
    '''
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    'username': user.username,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            else:
                raise serializers.ValidationError('Username yoki parol xato.')
        else:
            raise serializers.ValidationError('Username va parolni kiriting')

class StatusSerializer(serializers.ModelSerializer):
    '''
    Status modeli uchun serializer
    '''
    class Meta:
        model = Status
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    '''
    Teacher modeli uchun serializer
    '''
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), validators=[
        UniqueValidator(
            queryset=Teacher.objects.all(),
            message="Bu profil mavjud"
        )
    ])
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), help_text='Mutaxasislik')
    class Meta:
        model = Teacher
        fields = ['id', 'profile', 'status']

class ModeratorSerializer(TeacherSerializer):

    '''
    Moderator modeli uchun serializer
    '''
    class Meta:
        model = Moderator
        fields = ['id', 'profile', 'status']




class CategorySerializer(serializers.ModelSerializer):
    '''
    Kategoriya uchun serializer
    '''
    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    '''
    Course modeli uchun serializer
    '''
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    moderator = serializers.PrimaryKeyRelatedField(queryset=Moderator.objects.all())
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    lessons_count = serializers.SerializerMethodField()
    lesson_videos_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'category', 'teacher', 'moderator', 'students', 'name', 'description', 'price', 'duration', 'lessons_count', 'lesson_videos_count']

    def get_lessons_count(self, instance) -> int:
        '''
        Darslar sonini qaytaradi
        '''
        return instance.lesson_set.count()

    def get_lesson_videos_count(self, instance) -> int:
        '''
        Darslardagi videolar sonini qaytaradi
        '''
        lessons = instance.lesson_set.all()
        lesson_videos_count = sum(lesson.lessonvideo_set.count() for lesson in lessons)
        return lesson_videos_count

class LessonSerializer(serializers.ModelSerializer):
    '''
    Lesson modeli uchun serializer
    '''
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title']

class LessonVideoSerializer(serializers.ModelSerializer):
    '''
    Dars videosi uchun serializer
    '''
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    average_rating = serializers.FloatField(read_only=True)
    ratings_count = serializers.IntegerField( read_only=True)

    class Meta:
        model = LessonVideo
        fields = ['id', 'lesson', 'name', 'video', 'average_rating', 'ratings_count']

    def get_average_rating(self, obj):
        '''
        Ratinglarni ortacha qiymatini qaytaradi
        '''
        return obj.average_rating


    def to_representation(self, instance):
        '''
        Bu metod obyektni seriyal qilish jarayonida JSON formatdagi
        ozgartirilgan malumotlarni qaytaradi
        '''
        representation = super().to_representation(instance)
        ratings = instance.ratings.all()

        if ratings.exists():
            avg_rating = ratings.aggregate(Avg('score'))['score__avg']
            representation['average_rating'] = round(avg_rating, 2) if avg_rating is not None else None
            representation['ratings_count'] = ratings.count()
        else:
            representation['average_rating'] = None
            representation['ratings_count'] = 0

        return representation


class LessonHomeworkSerializer(serializers.ModelSerializer):
    '''
    LessonHomework modeli uchun serializer
    '''
    lesson_video = serializers.PrimaryKeyRelatedField(queryset=LessonVideo.objects.all())
    class Meta:
        model = LessonHomework
        fields = ['id', 'lesson_video', 'homework', 'file', 'deadline']

class HomeworkFromStudentSerialzier(serializers.ModelSerializer):
    '''
    HomeworkFromStudents modeli uchun serializer
    '''
    lesson_homework = serializers.PrimaryKeyRelatedField(queryset=LessonHomework.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = HomeworkFromStudent
        fields = ['lesson_homework', 'student', 'file', 'description']


class RatingSerializer(serializers.ModelSerializer):
    '''
    Rating uchun serializer
    '''
    lesson_video = serializers.PrimaryKeyRelatedField(queryset=LessonVideo.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    score = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        model = Rating
        fields = ['id', 'lesson_video', 'user', 'score']



class CommentSerializer(serializers.ModelSerializer):
    '''
    Comment uchun serializer
    '''
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'lesson', 'user', 'text', 'created']


