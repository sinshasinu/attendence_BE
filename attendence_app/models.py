import datetime

from django.db import models

# Create your models here.
class Attendance(models.Model):
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    total_break_hours = models.CharField(max_length=10, default="0:00")
    total_work_hours = models.CharField(max_length=10, null=True, blank=True, default="0:00")
    
    def calculate_total_break_hours(self):
        total_duration = datetime.timedelta()

        for break_obj in self.breaks.all():
            if break_obj.start_time and break_obj.end_time:
                total_duration += (break_obj.end_time - break_obj.start_time)

        # Convert to HH:MM format
        total_seconds = int(total_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}:{minutes:02d}"

    def calculate_total_work_hours(self):
        if self.check_in_time and self.check_out_time:
            total_duration = self.check_out_time - self.check_in_time


            break_duration = datetime.timedelta()

            for break_obj in self.breaks.all():
                if break_obj.start_time and break_obj.end_time:
                    break_duration += (break_obj.end_time - break_obj.start_time)

            work_duration = total_duration - break_duration

            # Convert to HH:MM format
            total_seconds = int(work_duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}:{minutes:02d}"

        return "0:00"



    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
class Break(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='breaks')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Break for {self.attendance.user.username} on {self.attendance.date}"