from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from .validators import validate_phone


class Profile(models.Model):
    '''
    Bu model foydalanuvchi profilini saqlaydi
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Foydalanuvchi')
    photo = models.ImageField(upload_to='profile_photos/', default='default_avatar/avatar.jpg', verbose_name='Rasm')
    full_name = models.CharField(max_length=255, verbose_name='Toliq ism')
    phone_number = models.CharField(max_length=13, validators=[validate_phone], verbose_name='Telefon raqam')
    address = models.CharField(max_length=255, verbose_name='Manzil', null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Status(models.Model):
    '''
    Bu model IT kasblar uchun
    '''
    name = models.CharField(max_length=255, verbose_name='Nomi')

    def __str__(self):
        return self.name




class Teacher(models.Model):
    '''
    Bu model oqituvchini malumotlarini saqlaydi
    '''
    profile = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, verbose_name='Profil')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Mutaxasisligi')

    def __str__(self):
        return f"Teacher: {self.profile}"



class Moderator(models.Model):
    '''
    Bu model moderator malumotlarini saqlaydi
    '''

    profile = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, verbose_name='Profil')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Mutaxasisligi')

    def __str__(self):
        return f"Moderator: {self.profile}"

class Category(models.Model):
    '''
    Bu model kurs kategoriyasi uchun
    '''
    name = models.CharField(max_length=255, verbose_name='Nomi')

    def __str__(self):
        return self.name

class Course(models.Model):
    '''
    Bu model kurs malumotlarini saqlaydi
    '''
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Kategoriya')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="O'qituvchi")
    moderator = models.ForeignKey(Moderator, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(User, blank=True, verbose_name="Oquvchilar")
    name = models.CharField(max_length=255, unique=True, verbose_name='Kurs nomi')
    description = models.TextField(blank=True, null=True, verbose_name='Malumot')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi", help_text='Bir oylik narx')
    duration = models.IntegerField(default=0, verbose_name="Davomiyligi")

    def __str__(self):
        return self.name

    def get_course_total_price(self):
        '''
        Kursning umumiy narxini qaytaradi
        '''
        return self.price * self.duration

    def get_lessons_count(self):
        '''
        Kursdagi darslar sonini qaytaradi
        '''
        return self.lesson_set.count()

    def get_lesson_videos_count(self, instance):
        '''
        Darsdagi videolar sonini qaytaradi
        '''
        lessons = instance.lesson_set.all()
        lesson_videos_count = sum(lesson.lessonvideo_set.count() for lesson in lessons)
        return lesson_videos_count



class Lesson(models.Model):
    '''
    Bu model dars malumotlarini saqlaydi
    '''
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True ,verbose_name='Kurs')
    title = models.CharField(max_length=255, verbose_name='Nomi')

    def __str__(self):
        return self.title



class LessonVideo(models.Model):
    '''
    Dars mavzu va videolari uchun
    '''
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, verbose_name="Dars")
    name = models.CharField(max_length=255, verbose_name="Mavzu")
    video = models.FileField(upload_to='lesson/videos/', validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'WMV'])
    ], verbose_name='Dars videosi', )


    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        '''
        Bu metod reytingni ortacha qiymatini qaytaradi
        agar reyting yoq bolsa 0 qaytaradi
        '''
        ratings = self.rating.all()
        if ratings.exists():
            return sum(rating.score for rating in ratings) / ratings.count()
        else:
            return 0

    def ratings_count(self):
        '''
        Bu metod reytinglar sonini qaytaradi
        '''
        return self.ratings.count()




class LessonHomework(models.Model):
    '''
    Bu model dars uyga vazifasini malumotlarini saqlaydi
    '''
    lesson_video = models.ForeignKey(LessonVideo, on_delete=models.SET_NULL, null=True, verbose_name="Dars videosi")
    homework = models.CharField(max_length=255, verbose_name='Uyga vazifa')
    file = models.FileField(upload_to='lesson/videos/homework/', validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'WMV', 'png', 'jpg', 'rar', 'zip'])
    ], null=True, blank=True,  verbose_name='Dars uyga vazifasi',)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')
    deadline = models.DateTimeField(verbose_name='Vazifa muddati')

    def __str__(self):
        return f"{self.lesson_video.name} -> {self.homework}"

class HomeworkFromStudent(models.Model):
    '''
    Bu model oquvchilar uyga vaifasini malumotlarini saqlaydi
    '''
    lesson_homework = models.ForeignKey(LessonHomework, on_delete=models.SET_NULL, null=True, verbose_name='Uyga vazifa')
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="O'quvchi")
    file = models.FileField(upload_to="lesson/videos/students-homework/", validators=[
        FileExtensionValidator(allowed_extensions=['rar', 'zip', 'png', 'jpg', 'mp4', 'WMV'])
    ], verbose_name='Fayl')
    description = models.CharField(max_length=255, verbose_name='Izoh')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')

    def __str__(self):
        return f"{self.student} -> {self.lesson_homework}"


    def clean(self):
        '''
        Bu metod vazifa muddati deadlindan otib ketgan bolsa
        ValidationError xatoligini ishga tushiradi
        '''
        super().clean()
        if timezone.now() > self.lesson_homework.deadline:
            raise ValidationError('Vazifa muddati otgan')

    def save(self, *args, **kwargs):
        '''
        Bu metod clean() - obyektni tozalab , super() metodi orqali asosiy classni
        save() metodi chaqiriladi va obyektni databasega saqlaydi
        '''
        self.clean()
        super().save(*args, **kwargs)


class Rating(models.Model):
    '''
    reyting uchun
    '''
    lesson_video = models.ForeignKey(LessonVideo, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  related_name='ratings')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ( 'lesson_video', 'user',)


    def __str__(self):
        return f"{self.lesson_video.name}->{self.score}"


class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Dars')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Foydalanuvchi')
    text = models.CharField(max_length=255, verbose_name='Izoh')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')

    def __str__(self):
        return f"{self.user} -> {self.lesson}"




