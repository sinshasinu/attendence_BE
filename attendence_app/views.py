from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from attendence_app.models import Attendance, Break
from attendence_app.serializers import AttendanceSerializer
from user_app.models import User
from rest_framework.authentication import TokenAuthentication


# 🔹 Attendance List
class AttendanceAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
       user = request.user

        # 🔹 Employee → only own data
       if user.role == 'employee':
            queryset = Attendance.objects.filter(user=user)

        # 🔹 Admin → all data
       elif user.role == 'admin':
            queryset = Attendance.objects.all()

       else:
            return Response({"error": "Invalid role"}, status=400)

       serializer = AttendanceSerializer(queryset, many=True)
       return Response(serializer.data)


# 🔹 Check-In API
class CheckInAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = timezone.now().date()

        attendance = Attendance.objects.filter(user=user, date=today).order_by("-id").first()

        if attendance:
            return Response({"error": "Already checked in"}, status=400)

        new_attendance = Attendance.objects.create(
            user=user,
            date=today,
            check_in_time=timezone.now(),
            total_work_hours=0,
            total_break_hours=0
        )

        return Response({
            "message": "Checked in successfully",
            "data": AttendanceSerializer(new_attendance).data
        }, status=201)


# 🔹 Check-Out API
class CheckOutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = timezone.now().date()

        attendance = Attendance.objects.filter(user=user, date=today, check_out_time__isnull=True).order_by("-id").first()

        if not attendance:
            return Response({"error": "Check-in required first"}, status=400)

        if attendance.check_out_time:
            return Response({"error": "Already checked out"}, status=400)
        

        if Break.objects.filter(attendance=attendance, end_time__isnull=True).exists():
            return Response({"error": "End break before checkout"}, status=400)

        attendance.check_out_time = timezone.now()
        attendance.total_break_hours = attendance.calculate_total_break_hours()
        attendance.total_work_hours = attendance.calculate_total_work_hours()

        attendance.save()
        return Response({
            "message": "Checked out successfully",
            "data": AttendanceSerializer(attendance).data
        })



# 🔹 Break API (start / end)
class BreakAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = timezone.now().date()

        attendance = Attendance.objects.filter(user=user, date=today).order_by("-id").first()

        if not attendance or not attendance.check_in_time:
            return Response({"error": "Check-in required first"}, status=400)
        
        if attendance.check_out_time:
            return Response({"error": "Cannot take brak after checkout"}, status=400)

        active_break = Break.objects.filter(
            attendance=attendance,
            end_time__isnull=True
        ).order_by("-id").first()

        # End break
        if active_break:
            active_break.end_time = timezone.now()
            active_break.save()

            attendance.total_break_hours = attendance.calculate_total_break_hours()
            attendance.total_work_hours = attendance.calculate_total_work_hours()
            attendance.save()

            return Response({
                "message": "Break ended",
                "data": AttendanceSerializer(attendance).data
            })

        #  Start break
        Break.objects.create(
            attendance=attendance,
            start_time=timezone.now()
        )

        return Response({
            "message": "Break started",
            "data": AttendanceSerializer(attendance).data
        })

