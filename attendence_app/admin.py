from django.contrib import admin
from .models import Attendance, Break

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'check_in_time', 'check_out_time']

@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ['attendance', 'start_time', 'end_time']
