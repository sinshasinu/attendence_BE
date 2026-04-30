from django.contrib import admin
from user_app.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:  # Only set password for new users
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)