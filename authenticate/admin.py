from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id', 'hometown', 'latitude', 'longitude', 'units')

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

# Register your custom UserProfileAdmin
admin.site.register(UserProfile, UserProfileAdmin)
