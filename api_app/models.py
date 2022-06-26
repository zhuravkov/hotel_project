from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """"USERNAME --- EMAIL полностью настраиваемая модель пользователя"""
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_regex = RegexValidator(regex=r'^((\+7)+([0-9]){10})$', message=
    "ФОРМАТ дожен быть: +79998885555")
    phone = models.CharField(validators=[phone_regex], verbose_name='Телефон',
                             max_length=12, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

#ROOMS CATEGORY
class Category(models.Model):
  title = models.CharField(max_length=100, verbose_name = 'Категория')
  content = models.TextField(verbose_name = 'Описание категории')
  image = models.ImageField(blank=True, upload_to='images/',
								verbose_name = 'Основное изображение для категории')
  
  def __str__(self):
        return self.title
  class Meta:
    verbose_name_plural = 'Категории'
    verbose_name = 'Категория'
