from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
#from django.contrib.auth import User
from django.core.mail import send_mail

# Create your models here.

class UserManager(BaseUserManager):
    '''
    UserManager class consists functions to create a new user
    '''
    # Allows django to use this UserManager within the migrations proccess
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email should be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    '''
    Custom User Class with fields below
    '''
    email = models.EmailField(unique=True, max_length=40)
    name = models.CharField(max_length=20)
    alias = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(auto_now=True, auto_created=True)
    birth_date = models.DateField(null=True, blank=True)
    authority_level = models.SmallIntegerField(default=1) # 1 is the minimum 9 is the admin
    is_active = models.BooleanField(default=True) # active account
    profile_image = models.ImageField(upload_to='profile_img/', null=True, blank=True)
    is_superuser = models.BooleanField(default=False) # django admin authority
    is_staff = models.BooleanField(default=False) # django admin access grant

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an Email to subject, with message
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self) -> str:
        return f"{self.name} {self.email} {self.alias} {self.date_joined}"