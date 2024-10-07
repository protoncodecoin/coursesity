import uuid
import redis
from django.db.models import Count
from django.conf import settings

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
    MeetingSerializer,
    RatingSerializer,
    SubjectSerializer,
    CourseSerializer,
    WishListSerializer,
)
from courses.models import Subject, Course, Rating
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentsSerializer
from students.models import WishList
from users.models import Meeting

from courses.tasks import notify_meeting_participants

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


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

        # Validate rating_value
        if rating_value is None or rating_value not in [1, 2, 3, 4, 5]:
            return Response(
                {"error": "Invalid rating value"}, status=status.HTTP_400_BAD_REQUEST
            )

        # get course from database
        course_obj = Course.objects.filter(id=course_id).first()
        if not course_obj:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )

        rating, created = Rating.objects.update_or_create(
            course=course_obj,
            user=user,
            defaults={"rating": rating_value, "comment": comment, "user": user},
        )
        if created:
            return Response(
                {"created": True, "updated": False}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"created": False, "updated": True}, status=status.HTTP_200_OK
            )


class CheckRatingStatus(views.APIView):
    """
    Check feature a student as rated a course or not.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        course_id = request.GET.get("course_id")
        course_obj = Course.objects.filter(id=course_id).first()
        # check if user has rated the course
        is_rated = Rating.objects.filter(course=course_id, user=user).exists()

        if is_rated:
            return Response({"rating_status": True, "course_id": course_id})
        return Response({"rating_status": False, "course_id": course_id})


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
            wishlist_obj = WishList.objects.get(course=course_obj, user=user)
            wishlist_obj.delete()
            return Response({"action": "deleted"}, status=status.HTTP_200_OK)

        # add to wishlist
        WishList.objects.create(user=user, course=course_obj)
        return Response({"action": "created"}, status=status.HTTP_201_CREATED)


class MeetingForCourse(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        meetings = Meeting.objects.all()
        meetings_serializer = MeetingSerializer(meetings, many=True)
        return Response(meetings_serializer.data)

    def post(self, request):
        user = request.user
        course_id = request.data.get("course")
        meeting_name = request.data.get("meeting_name")
        restriction = request.data.get("is_restricted", True)
        about_message = request.data.get("about_message", "No message added")
        sch_date = request.data.get("sch_date")
        sch_time = request.data.get("sch_time")

        if user and user.is_instructor or user.is_admin:
            course_obj = Course.objects.filter(id=course_id).first()
            if course_obj:

                if meeting_name == "" or meeting_name is None:
                    meeting_name = course_obj.title
                # create meeting
                meeting_token = uuid.uuid4()
                new_meeting = Meeting.objects.create(
                    host=user,
                    meeting_token=meeting_token,
                    course=course_obj,
                    only_enrolled_students=restriction,
                    about_message=about_message,
                    meeting_name=meeting_name,
                    sch_date=sch_date,
                    sch_time=sch_time,
                )
                new_meeting.save()

                # send email notification to all enrolled students
                notify_meeting_participants.delay(course_id, new_meeting.id)

                return Response({"token": meeting_token})
            return Response({"error": "course not found"})
        return Response({"error": "Unauthorizied"})


class SaveStudentProgress(views.APIView):
    """
    Save student progress
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        module_id = request.data.get("module_id")

        course = Course.objects.filter(id=course_id).first()

        if module_id:
            last_module_key = f"user:{request.user.id}:last_module:{course.id}"
            r.set(last_module_key, module_id)

            return Response({"progress_status": "saved"})
        return Response({"progress_status": "error"})
