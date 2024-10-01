# from django.contrib.auth.forms import UserCreationForm
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
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from courses.models import Course

from users.forms import CustomUserCreationForm

# Create your views here.


# class StudentLoginView(TemplateResponseMixin, View):
#     template_name = "students/student/login.html"

#     def get(self, request, *args, **kwargs):
#         return self.render_to_response({})

#     def post(self, request, *args, **kwargs):
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # authenticate user
#         user = authenticate(request, email=email, password=password)

#         if user and user.is_active:
#             login(request, user)
#             return redirect("student_course_list")

#         messages.error(request, "Invalid credentials provided")
#         return redirect("student_registration")


# class StudentRegistrationView2(TemplateResponseMixin, View):
#     template_name = "students/student/registration.html"

#     def get(self, request, *args, **kwargs):
#         return self.render_to_response({})


#     def post(self, request, *args, **kwargs):
#         first_name = request.POST.get("firstName")
#         last_name = request.POST.get("last_name")
#         email = request.POST.get("email")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")

#         # validate email
#         if get_user_model().objects.filter(email=email).exists():
#             messages.error(request, "Email is already registered")
#             return redirect("student_registration")

#         # validate password
#         if password1 != password2:
#             messages.error(request, "Passwords do not match!")
#             return redirect("student_registration")

#         try:
#             validate_password(password1)
#         except ValidationError as e:
#             messages.error(request, str(e))
#             return redirect("student_registration")

#         return redirect("student_course_list")


# class StudentRegistrationView(CreateView):
#     template_name = "students/student/registration.html"
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("student_course_list")

#     def form_valid(self, form):
#         result = super().form_valid(form)
#         cd = form.cleaned_data
#         user = authenticate(username=cd["email"], password=cd["password1"])

#         # get session and store session
#         cart = self.request.session.get(settings.CART_SESSION_ID, [])

#         login(self.request, user)

#         # Restore the cart data to the new session
#         if cart:
#             self.request.session = cart

#             next_url = self.request.session.get("next", "orders:order_create")

#             return redirect(next_url)

#         return result


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
    template_name = "students/course/list2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "student_content"
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "students/course/detail2.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        context["style"] = "content_list"
        context["style2"] = "base2"
        if "module_id" in self.kwargs:
            # get current module
            context["module"] = course.modules.get(id=self.kwargs["module_id"])
        else:
            # get first module
            context["module"] = course.modules.all()[0]
        return context
