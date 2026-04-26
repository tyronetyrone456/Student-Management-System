from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Course, Enrollment, TuitionFee
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer, TuitionFeeSerializer

def index(request):
    return render(request, 'students/base.html')

@method_decorator(csrf_exempt, name='dispatch')
class CsrfExemptModelViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

class CourseViewSet(CsrfExemptModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentViewSet(CsrfExemptModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class EnrollmentViewSet(CsrfExemptModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        enrollment = serializer.save()
        student = enrollment.student
        if student.course_id != enrollment.course_id:
            student.course = enrollment.course
            student.save(update_fields=['course'])
        TuitionFee.objects.get_or_create(student=student)

    def perform_update(self, serializer):
        enrollment = serializer.save()
        student = enrollment.student
        if student.course_id != enrollment.course_id:
            student.course = enrollment.course
            student.save(update_fields=['course'])

    def perform_destroy(self, instance):
        student = instance.student
        instance.delete()
        if not Enrollment.objects.filter(student=student).exists():
            TuitionFee.objects.filter(student=student).delete()

class TuitionFeeViewSet(CsrfExemptModelViewSet):
    queryset = TuitionFee.objects.all()
    serializer_class = TuitionFeeSerializer

    @action(detail=True, methods=['post'], url_path='pay')
    def pay(self, request, pk=None):
        tuition = get_object_or_404(TuitionFee, pk=pk)
        amount = request.data.get('amount', 0)
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        tuition.amount_paid = float(tuition.amount_paid) + amount
        tuition.save()
        return Response({
            'message': 'Payment recorded',
            'amount_paid': tuition.amount_paid,
            'student': tuition.student.id
        }, status=status.HTTP_200_OK)