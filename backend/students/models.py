from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    units = models.IntegerField()
    fee_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    year_level = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    term = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Enrolled')

    def __str__(self):
        return f"{self.student} - {self.course}"

class TuitionFee(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def balance(self):
        if self.student.course:
            total = self.student.course.units * self.student.course.fee_per_unit
            return total - self.amount_paid
        return 0

    def __str__(self):
        return f"Tuition - {self.student}"