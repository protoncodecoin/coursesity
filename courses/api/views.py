from django.db.models import Count
from django.contrib import messages

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import views
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from courses.api.pagination import StandardPagination
from courses.api.serializers import (
    RatingSerializer,
    SubjectSerializer,
    CourseSerializer,
    WishListSerializer,
)
from courses.models import Subject, Course, Rating
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentsSerializer
from students.models import WishList


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count("courses"))
    serializer_class = SubjectSerializer
    pagination = StandardPagination


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related("modules")
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"enrolled": True})

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled],
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RatingAPIView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        ratings = Rating.objects.all()
        rating_serailizer = RatingSerializer(ratings, many=True)
        return Response(rating_serailizer.data)

    def post(self, request):
        user = request.user
        course_id: int = request.data.get("course")
        rating_value: int = request.data.get("rating")
        comment: str = request.data.get("comment")

        # get course from database
        course_obj = Course.objects.filter(id=course_id).first()

        rating, created = Rating.objects.update_or_create(
            course=course_obj,
            user=user,
            defaults={"rating": rating_value, "comment": comment},
        )
        if created:
            return Response({"created": True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"created": False}, status=status.HTTP_200_OK)


class WishAPIView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        qs = WishList.objects.filter(user=user)
        serializied_qs = WishListSerializer(qs, many=True)
        return Response(serializied_qs.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        course_id = request.data.get("course")
        course_obj = Course.objects.filter(id=course_id).first()

        # check if user has already added course to wish list
        wish_item = WishList.objects.filter(course=course_obj, user=user).exists()
        if wish_item:
            # remove course from wishlist
            WishList.objects.delete(course=course_obj, user=user)
            return Response({"action": "deleted"}, status=status.HTTP_200_OK)

        # add to wishlist
        WishList.objects.create(user=user, course=course_obj)
        return Response({"action": "created"}, status=status.HTTP_201_CREATED)
