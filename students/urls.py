from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    # path(
    #     "register/",
    #     views.StudentRegistrationView2.as_view(),
    #     name="student_registration",
    # ),
    # path("login/", views.StudentLoginView.as_view(), name="student_login"),
    path(
        "enroll-course/",
        views.StudentEnrollCourseView.as_view(),
        name="student_enroll_course",
    ),
    path(
        "courses/",
        views.StudentCourseListView.as_view(),
        name="student_course_list",
    ),
    path(
        "course/<pk>/",
        # cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        views.StudentCourseDetailView.as_view(),
        name="student_course_detail",
    ),
    path(
        "course/<pk>/<module_id>/",
        # cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        views.StudentCourseDetailView.as_view(),
        name="student_course_detail_module",
    ),
    # path("course/<pk>/quiz/<quiz_id>/"),
]
