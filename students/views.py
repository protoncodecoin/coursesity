import redis
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings


from courses.models import Course


# r = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB,
# )

REDIS_URL = getattr(settings, "REDIS_URL", "redis://localhost:6379/1")

r = redis.Redis.from_url(REDIS_URL)


# Create your views here.
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

        total_modules = course.modules.count()

        # Get last accessed module from Redis
        key = f"user:{self.request.user.id}:last_module:{course.id}"
        last_module_id = r.get(key)

        # Compute completed modules
        completed_modules = 0
        if last_module_id:
            completed_modules = course.modules.filter(id__lte=last_module_id).count()

        # Calculate progress percentage
        progress = (completed_modules / total_modules) * 100 if total_modules > 0 else 0

        # Store the progress in context
        context["progress"] = progress

        # Check if module_id is in kwargs, and get the corresponding module
        module_id = self.kwargs.get("module_id")

        if module_id:
            context["module"] = get_object_or_404(course.modules, id=module_id)
        else:
            # If no module_id is present, check Redis for last accessed module
            last_module_key = f"user:{self.request.user.id}:last_module:{course.id}"
            last_module_id = r.get(last_module_key)

            if last_module_id:
                context["module"] = get_object_or_404(course.modules, id=last_module_id)

            else:
                # Default to the first module if no last module is found
                context["module"] = course.modules.first()

        # if "module_id" in self.kwargs:
        #     # get current module
        #     context["module"] = course.modules.get(id=self.kwargs["module_id"])
        # else:
        #     # get first module
        #     context["module"] = course.modules.all()[0]

        context["style"] = "content_list"
        context["style2"] = "base2"

        return context
