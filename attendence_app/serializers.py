from rest_framework import serializers
from attendence_app.models import Attendance, Break
from user_app.models import User
from rest_framework.authtoken.models import Token

from user_app.serializers import UserSerializer
""" from attendence_app.serializers import BreakSerializer
 """

class BreakSerializer(serializers.ModelSerializer):

    class Meta:
        model = Break
        fields = [
            'attendance',
            'start_time',
            'end_time',
        ]
        read_only_fields = ['attendance']
        

class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    breaks = BreakSerializer(many=True, read_only=True)
    class Meta:
        model = Attendance
        fields = [
            'id',
            'user',
            'date',
            'check_in_time',
            'check_out_time',
            'total_break_hours',
            'total_work_hours',
            'breaks',

        ]
        read_only_fields = ['total_break_hours', 'total_work_hours']

    def get_user(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name if name else obj.user.username

    def get_breaks(self, obj):
        breaks = obj.breaks.all()
        return BreakSerializer(breaks, many=True).data