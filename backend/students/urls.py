from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CourseViewSet, EnrollmentViewSet, TuitionFeeViewSet, index

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'tuition', TuitionFeeViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]