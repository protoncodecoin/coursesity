from django.urls import include, path

from rest_framework import routers
from . import views

app_name = "courses"

router = routers.DefaultRouter()
router.register("courses", views.CourseViewSet)
router.register("subject", views.SubjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("rating/", views.RatingAPIView.as_view(), name="coures_rating"),
    path("wishlist/", views.WishAPIView.as_view(), name="wish_list"),
    path(
        "rating_status/", views.CheckRatingStatus.as_view(), name="check_rating_status"
    ),
    path(
        "create_meeting/",
        views.MeetingForCourse.as_view(),
        name="create_new_course_meeting",
    ),
    path(
        "verify-transaction/",
        views.VerifyPayStackTransaction.as_view(),
        name="verify_transaction",
    ),
    path("create-order/", views.CreateOrderAPI.as_view(), name="create_order_api"),
    path("save_progress/", views.SaveStudentProgress.as_view(), name="user_progress"),
    path("subject-titles/", views.SubjectTitleAPIView.as_view(), name="subject_titles"),
    path(
        "video-token-builder/",
        views.RTCTokenBuilderView.as_view(),
        name="token_builder",
    ),
]
