import datetime
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import DateTimeField
from django.forms import ValidationError
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
  price = models.PositiveSmallIntegerField(verbose_name="Цена")
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

#SEASON RATIO TEST
class SeasonRatio(models.Model):
  start_date = models.DateField(verbose_name="Начало")
  end_date = models.DateField(verbose_name="Конец")
  ratio = models.DecimalField(
                          verbose_name="Коэффициент",
                         max_digits = 3,
                         decimal_places = 2,
                        )


  def __str__(self) :
    return f'{self.start_date} - {self.end_date} - коэффициент {self.ratio}'

  class Meta:
    verbose_name_plural = 'Сезонные коэффициенты'
    verbose_name = 'Сезонный коэффициент'
    ordering = ['start_date',]


class Room (models.Model):
  category = models.ForeignKey(Category, on_delete = models.CASCADE,
						related_name='number_category'	, verbose_name = 'Категория')
  number = models.PositiveSmallIntegerField(verbose_name="№ аппартаментов")

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
	"Phone number must be entered in the format: '+79998882255'. Up to 10 digits allowed.")
  phone = models.CharField(validators=[phone_regex], max_length=12, verbose_name= 'Телефон покупателя') 
  agreement = models.BooleanField(verbose_name="согласие на обработку данных")
  paid = models.BooleanField(verbose_name="Заказ оплачен")
  done = models.BooleanField(verbose_name="Заказ исполнен")

  class Meta:
    verbose_name= 'Заказ'
    verbose_name_plural= 'Заказы'

  def __str__(self) :
    return "Заказ №" + str(self.id)

  # @property
  def get_Days(self):
    return (self.departure_date - self.arrival_date).days+1
  get_Days.short_description = 'Количество дней'




  def get_Price(self):
    base_price = self.room.category.price
    ratio = SeasonRatio.objects.all()

    each_day_of_order = []
    delta = self.departure_date - self.arrival_date
    # извлекаем каждый день из периода и делаем из них массив
    for i in range(delta.days + 1):
      each_day_of_order.append(self.arrival_date + datetime.timedelta(i))
    
    all_price_array =[]
    # к каждому дню ищем свой коэффициент и добавляем
    #  в массив итоговую стоимость конкретного дня
    for day in each_day_of_order:
      if ratio.exists:
        current_ratio = ratio.filter( start_date__lte = day, end_date__gte=day).first().ratio
      else:
        current_ratio = 1
      all_price_array.append(current_ratio*base_price)
    
    # возвращаем сумму за период
    return round(sum(all_price_array))
   
  get_Price.short_description = 'Стоимость'


  def clean(self):
    if not Order.objects.filter(pk=self.pk).exists():
      if check_avalibility(self.room, self.arrival_date, self.departure_date)==False:
        raise ValidationError("Выберете другие даты или номер (на указанный период номер забронирован)")

#Checking booking DATE
def check_avalibility (room, arrival_date, departure_date):
  avail_list = []
  order_list = Order.objects.filter(room=room)
  for order in order_list:
    if order.arrival_date > departure_date or order.departure_date < arrival_date:
      avail_list.append(True)
    else:
      avail_list.append(False)
  return all(avail_list)
