from rest_framework import serializers
from .models import Student, Course, Enrollment, TuitionFee

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)
    class Meta:
        model = Student
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_course_name(self, obj):
        return obj.course.name

    class Meta:
        model = Enrollment
        fields = '__all__'

class TuitionFeeSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    total_fee = serializers.SerializerMethodField()

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_balance(self, obj):
        return obj.balance()

    def get_total_fee(self, obj):
        if obj.student.course:
            return obj.student.course.units * obj.student.course.fee_per_unit
        return 0

    class Meta:
        model = TuitionFee
        fields = '__all__'