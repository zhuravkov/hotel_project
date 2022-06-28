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

  def delete(self, *args, **kwargs):
    """Удаление дополнительных изображений после удаления статьи"""
    for ai in self.additionalImg.all():
      ai.delete()
      super().delete(*args, **kwargs)

#MORE IMG FOR CATEGORY
class AdditionalImage(models.Model):
  category = models.ForeignKey(Category, on_delete = models.CASCADE,
						related_name='additionalImg'	, verbose_name = 'Категория')
  image = models.ImageField(upload_to='images/',
								verbose_name = 'Изображение')
  class Meta:
    verbose_name_plural = 'Дополнительные иллюстрации'
    verbose_name = 'Дополнительная иллюстрация'

class Room (models.Model):
  category = models.ForeignKey(Category, on_delete = models.CASCADE,
						related_name='number_category'	, verbose_name = 'Категория')
  number = models.PositiveSmallIntegerField(verbose_name="№ аппартаментов")
  price = models.PositiveSmallIntegerField(verbose_name="Цена")

  class Meta:
    verbose_name_plural = 'Номера'
    verbose_name = 'Номер'

  def __str__(self) :
    return "Номер " + str(self.number) + " - " + str(self.category.title)

# ORDER
class Order(models.Model):
  room = models.ForeignKey(Room, on_delete = models.CASCADE,
						related_name='order_room'	, verbose_name = 'Номер')
  arrival_date = models.DateField(verbose_name="Дата заезда")
  departure_date = models.DateField(verbose_name="Дата отъезда")
  adult =  models.PositiveSmallIntegerField(verbose_name="Количество взрослых")
  childeren = models.PositiveSmallIntegerField(verbose_name="Количество детей")
  child_age = models.CharField(max_length=100, verbose_name = 'Возраст детей')
  client_name = models.CharField(max_length=100, verbose_name = 'Имя клиента')
  phone_regex = RegexValidator(regex=r'^((\+7)+([0-9]){10})$',message=
	"Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
  phone = models.CharField(validators=[phone_regex], max_length=12, verbose_name= 'Телефон покупателя') 
  agreement = models.BooleanField(verbose_name="согласие на обработку данных")

  class Meta:
    verbose_name= 'Заказ'
    verbose_name_plural= 'Заказы'

  def __str__(self) :
    return "Заказ №" + str(self.id) 