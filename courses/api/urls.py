from django.urls import include, path

from rest_framework import routers
from . import views

app_name = "courses"

router = routers.DefaultRouter()
router.register("courses", views.CourseViewSet)
router.register("subject", views.SubjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path(
    #     "courses/<pk>/enroll/", views.CourseEnrollView.as_view(), name="course_enroll"
    # ),
]
