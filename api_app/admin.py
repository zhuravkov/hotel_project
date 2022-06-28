from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import AdditionalImage, Category, CustomUser, Order, Room


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Телефон', {'fields': ('phone',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','phone')},
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class AdditionalImageInline(admin.TabularInline):
	model = AdditionalImage
class CategoryAdmin(admin.ModelAdmin):
	inlines = (AdditionalImageInline,)


class RoomAdmin(admin.ModelAdmin):
  model = Room
  list_display = ('__str__', 'price')

class OrderAdmin(admin.ModelAdmin):
  model = Order
  list_display = ('__str__', 'room','arrival_date', 'departure_date','phone')
  
  # def formfield_for_foreignkey(self, db_field, request, **kwargs):
  #   if db_field.name == "order":
  #     kwargs["queryset"] = Order.objects.filter(in_work=False, is_done=False)
  #   return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category,CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
