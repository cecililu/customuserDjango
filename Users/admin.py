from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm




from django.contrib.admin.views.main import ChangeList



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'name', 'is_staff', 'is_active', 'is_CDO', 'is_Municipality', 'is_Ward', 'is_cluster', 'cluster_type', 'ward', 'municipality')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'name', 'is_staff', 'is_active', 'is_CDO', 'is_Municipality', 'is_Ward', 'is_cluster', 'cluster_type', 'ward', 'municipality')

class CustomUserAdmin(UserAdmin):
    
 
    
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined', 'updated_at', 'is_CDO', 'is_Municipality', 'is_Ward', 'is_cluster', )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_CDO', 'is_Municipality', 'is_Ward', 'is_cluster', 'cluster_type')
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name' ,'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_CDO', 'is_Municipality', 'is_Ward', 'is_cluster', 'cluster_type', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_CDO', 'is_Municipality', 'is_Ward', 'is_cluster')

admin.site.register(CustomUser, CustomUserAdmin)