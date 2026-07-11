from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    EnrollmentViewSet,
    StudentViewSet,
)

router = DefaultRouter()

router.register("courses", CourseViewSet)

router.register("students", StudentViewSet)

router.register("enrollments", EnrollmentViewSet)

urlpatterns = router.urls
