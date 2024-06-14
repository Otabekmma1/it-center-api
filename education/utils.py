from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from IT_CENTER import settings

def send_email(user, subject, template_name, context):
    '''
    Emailga xabar yuborish uchun
    '''
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


