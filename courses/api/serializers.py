from django.db.models import Count
from rest_framework import serializers

from courses.models import Rating, Subject, Course, Module, Content
from students.models import WishList


class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        courses = obj.courses.annotate(total_students=Count("students")).order_by(
            "total_students"
        )[:3]

        return [f"{c.title} ({c.total_students})" for c in courses]

    class Meta:
        model = Subject
        fields = [
            "id",
            "title",
            "slug",
            "total_courses",
            "popular_courses",
        ]


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["order", "title", "description"]


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
            "modules",
        ]


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ["order", "item"]


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ["order", "title", "description", "contents"]


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
            "modules",
        ]


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
        ]


class WishListSerializer(serializers.ModelSerializer):
    course = SimpleCourseSerializer()
    rating = serializers.ReadOnlyField(source="course.average_rating")

    class Meta:
        model = WishList
        fields = [
            "user",
            "course",
            "rating",
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            "user",
            "course",
            "rating",
        ]
