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
]
