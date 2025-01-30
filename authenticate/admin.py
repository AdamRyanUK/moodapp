from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id', 'hometown', 'lat', 'lon', 'units', 'first_login')

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

# Register your custom UserProfileAdmin
admin.site.register(Profile, ProfileAdmin)