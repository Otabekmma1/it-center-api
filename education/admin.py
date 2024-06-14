from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'phone_number', 'address', 'telegram', 'get_image']
    list_display_links = ['id', 'user', 'full_name']
    search_fields = ['id', 'full_name', 'user']


    def get_image(self, profile):
        if profile.photo:
            return mark_safe(f'<img src="{profile.photo.url}" width="75px;">')
        return '-'

    get_image.short_description = 'Rasmi'


@admin.register(Status, Category)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_display_links = ['id', 'name']

@admin.register(Teacher, Moderator)
class TeacherModeratorAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'status']
    list_editable = ['status']
    list_display_links = ['profile', 'id']
    search_fields = ['profile', 'id', 'status']
    list_filter = ['status']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'teacher', 'moderator', 'name', 'description', 'price', 'duration']
    list_editable = ['category']
    search_fields = ['id', 'category', 'teacher', 'moderator', 'name', 'students']
    list_filter = ['price', 'category', 'teacher', 'moderator']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'title']
    search_fields = ['id', 'title']
    list_filter = ['course']

@admin.register(LessonVideo)
class LessonVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'name', 'get_video']
    list_filter = ['lesson']
    search_fields = ['id', 'lesson', 'name']
    list_display_links = ['lesson']
    def get_video(self, lessonvideo):
        if lessonvideo.video:
            return mark_safe(f'<video src="{lessonvideo.video.url}" width="75px;" controls></video>')
        return '-'

    get_video.short_description = 'Video'

@admin.register(LessonHomework)
class LessonHomeworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson_video', 'homework', 'created', 'deadline', 'get_file']
    list_filter = ['created', 'deadline', 'lesson_video']
    search_fields = ['id', 'lesson_video', 'homework']

    def get_file(self, lessonhomework):
        if lessonhomework.file:
            return mark_safe(f'<video src="{lessonhomework.file.url}" width="75px;" controls></video>')
        return '-'

    get_file.short_description = 'Video'


@admin.register(HomeworkFromStudent)
class HomeworkFromStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson_homework', 'student', 'description', 'created', 'file']
    list_filter = ['created', 'lesson_homework', 'student']
    list_display_links = ['lesson_homework']
    search_fields = ['id', 'lesson_homework', 'student', 'description']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson_video', 'user', 'score']
    list_filter = ['lesson_video', 'user', 'score']
    list_display_links = ['lesson_video']
    search_fields = ['id', 'lesson_video', 'user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'user']
    list_filter = ['lesson', 'created']
    search_fields = ['lesson', 'id', 'text']
    list_display_links = ['lesson', 'id']

