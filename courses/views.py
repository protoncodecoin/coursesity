from django.shortcuts import render
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Course


# Create your views here.
class OwnerMixin:
    """Filter queryset based on the current request.user"""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    """check the validilty of forms and set the owner attribute of the object to the current user"""

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    returns a form template to be used.
    """

    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = "courses/manage/course/list.html"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    Create a new course.
    It uses the form template from the OwnerCourseEditMixin
    """

    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    Update an already existing course.
    It uses the form template from the OwnerCourseEditMixin
    """

    pass


class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
