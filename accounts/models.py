from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail  
from django.conf import settings
import random
from django.core.cache import cache
# Create your models here.

class User(AbstractBaseUser):
    username = models.CharField(max_length=50,default='')
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email_token = models.CharField(max_length=200, null=True, blank=True)
    forget_password  = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    credits = models.IntegerField(default=100)
    rating = models.FloatField(default=0.0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def name(self):
        return self.username
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

def otp_mail(email, user):
    if cache.get(email):
        return False
    otp = random.randint(1000,9999)
    cache.set(email, otp, timeout=60)
    user.otp = otp
    user.save()
    subject = 'Your email needs to be verified'
    message = f'Your otp to verify your email is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)    
    return True

@receiver(post_save, sender = User)
def send_mail_otp(sender, instance, created, **kwargs):
    if created:
        try:
            otp = random.randint(1000,9999)
            # cache.set(instance.email, otp, timeout=60)
            instance.otp = otp
            instance.save()
            subject = 'Your email needs to be verified'
            message = f'Your otp to verify your email is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email]
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            print(e)