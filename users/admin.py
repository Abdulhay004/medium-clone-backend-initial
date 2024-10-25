from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Follow, Notification

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

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read_at')  # Customize fields to display
    search_fields = ('user__username', 'message')  # Enable search by username and message
    list_filter = ('read_at', 'created_at')  # Add filters for read status and creation date
admin.site.register(Notification, NotificationAdmin)
