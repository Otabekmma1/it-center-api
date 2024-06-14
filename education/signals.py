from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Course, Profile
from .utils import send_email

@receiver(post_save, sender=Course)
def course_send_email(sender, instance, created, **kwargs):
    '''
    Bu signal orqali avtomatik tarzda yangi qoshilgan yoki yangilangan kurslar haqida
    barcha foydalanuvchilarning emailga xabar yuboriladi
    '''
    users = User.objects.all()
    if created:
        subject = 'Yangi kurs qoshildi!'
        template_name = 'email.html'
    else:
        subject = 'Kurs yangilandi!'
        template_name = 'update_email.html'

    for user in users:
        send_email(
            user=user,
            subject=subject,
            template_name=template_name,
            context={'course': instance, 'user': user, 'subject': subject, }
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    '''
    yangi user hosil boganda uni profilga qoshadi
    '''
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()