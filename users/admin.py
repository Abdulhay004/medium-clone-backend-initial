from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Follow

@admin.register(CustomUser)   # administrator panelida ro'yxatdan o'tdan o'tkazish
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('middle_name', 'avatar',)
        }),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'middle_name')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'middle_name')
    list_filter = ('last_login', 'date_joined', 'is_staff', 'is_superuser', 'is_active')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followee', 'username', 'first_name', 'last_name', 'middle_name', 'email', 'avatar')
    search_fields = ('follower__username', 'followee__username')
admin.site.register(Follow, FollowAdmin)
