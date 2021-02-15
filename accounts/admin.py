from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'avatar']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('phone_number', 'address', 'avatar')}),
    )

admin.site.register(get_user_model(), CustomUserAdmin)
