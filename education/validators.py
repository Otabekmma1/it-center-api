from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User


def validate_phone(number):
    '''
    Telefon raqami +998XXXXXXXXX formatga tekshiradi
    '''
    phone = re.compile(r'^\+998\d{9}$')
    if not phone.match(number):
        raise ValidationError("Telefon raqam '+998XXXXXXXXX' formatda bo'lishi kerak !!!")


def validate_password(password):
    '''
    Parolni validatsiya qiladi quyidagi shartlarga
    '''
    if len(password) < 8:
        raise ValidationError(
            ("Parol 8 ta dan kam bomasligi kerak!!! "),
            params={'password': password}
        )

    if not re.search(r'\d', password):
        raise ValidationError(
            ("Parolda raqam ham qatnashishi kerak."),
            params={'password': password},
        )
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            ("Parolda bosh harf ham bo'lishi kerak."),
            params={'password': password},
        )
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            ("Parolda kichik harf ham bolishi kerak"),
            params={'password': password},
        )
    if not re.search(r'[\W_]', password):
        raise ValidationError(
            ("Parolda kamida bitta maxsus belgi ham bolishi kerak."),
            params={'password': password},
        )

def validate_email(email):
    """
    Emailni oldin royxatdan otganligiga tekshiradi.
    """
    if User.objects.filter(email=email).exists():
        raise ValidationError("BU email orqali avval royxatdan otilgan")
    return email


