from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateResponseMixin, View

from courses.models import Course

# Create your views here.


# class StudentLoginView(TemplateResponseMixin, View):
#     template_name = "students/student/registration.html"

#     def post(self, request, *args, **kwargs):
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # check if user is in databse
#         user = get_user_model()
#         existing_user = user.objects.filter(email=email).exists()
#         if existing_user:
#             auth_user = authenticate(request, email, password)

#             if auth_user is not None:

#                 login(request, auth_user)

#                 return redirect()


class StudentRegistrationView(CreateView):
    template_name = "students/student/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("student_course_list")

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd["username"], password=cd["password1"])

        # get session and store session
        cart = self.request.session.get(settings.CART_SESSION_ID, [])

        login(self.request, user)

        # Restore the cart data to the new session
        if cart:
            self.request.session = cart

            next_url = self.request.session.get("next", "orders:order_create")

            return redirect(next_url)

        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("student_course_detail", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "students/course/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if "module_id" in self.kwargs:
            # get current module
            context["module"] = course.modules.get(id=self.kwargs["module_id"])
        else:
            # get first module
            context["module"] = course.modules.all()[0]
        return context
