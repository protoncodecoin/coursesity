from datetime import timedelta
from django.http.response import HttpResponse as HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.apps import apps
from django.forms.models import modelform_factory
from django.db.models import Count, OuterRef, Subquery, Sum
from django.core.cache import cache
from django.shortcuts import render
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)


from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from courses.recommender import Recommender
from quiz.models import Quiz
from students.forms import CourseEnrollForm
from students.models import WishList


from .models import Course, Module, Content, Rating, Subject
from .forms import ModuleFormset


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


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ["subject", "title", "slug", "overview", "price"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    returns a form template to be used.
    """

    template_name = "courses/manage/course/form2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "create_form"
        return context


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = "courses/manage/course/list2.html"
    permission_required = "courses.view_course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "manage_course"
        return context


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    Create a new course.
    It uses the form template from the OwnerCourseEditMixin
    """

    permission_required = "courses.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    Update an already existing course.
    It uses the form template from the OwnerCourseEditMixin
    """

    permission_required = "courses.change_course"


class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"

    permission_required = "courses.delete_course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "create_form"
        return context


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = "courses/manage/module/formset2.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormset(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {
                "course": self.course,
                "formset": formset,
                "style": "course_form",
            }
        )

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_course_list")
        return self.render_to_response(
            {
                "course": self.course,
                "formset": formset,
                "style": "course_form",
            }
        )


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = "courses/manage/content/form2.html"

    def get_model(self, model_name):
        if model_name in ["text", "video", "file", "image"]:
            return apps.get_model(app_label="courses", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model,
            exclude=[
                "owner",
                "order",
                "created",
                "updated",
            ],
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {
                "form": form,
                "object": self.obj,
                "style": "create_form",
            }
        )

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model, instance=self.obj, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
                return redirect("module_content_list", self.module.id)
            return self.render_to_response(
                {
                    "form": form,
                    "object": self.obj,
                    "style": "create_form",
                }
            )


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect("module_content_list", module.id)


class ModuleContentListVIew(TemplateResponseMixin, View):
    template_name = "courses/manage/module/content_list2.html"

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response(
            {
                "module": module,
                "style": "content_list",
                "style2": "base2",
            }
        )


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({"saved": "OK"})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(
                order=order
            )
        return self.render_json_response({"saved": "OK"})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = "courses/course/list2.html"
    MAX_SIZE: int = 9

    def get(self, request, subject=None):
        subjects = cache.get("all_subjects")
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count("courses"))
            cache.set("all_subjects", subjects)

        all_courses = Course.objects.annotate(total_modules=Count("modules"))

        # get all popular courses
        popular_courses = cache.get("popular_courses")
        if not popular_courses:

            popular_courses = (
                all_courses.annotate(num_of_students=Count("students"))
                .order_by("-num_of_students")
                .filter(num_of_students__gte=1)[: self.MAX_SIZE]
            )
            cache.set("popular_courses", popular_courses)

        # get recently added courses
        recently_added = cache.get("recently_added")
        if not recently_added:
            self.MAX_SIZE = 9
            QUERY_DATE = timezone.now() - timedelta(days=30)

            recently_added = all_courses.filter(created__gte=QUERY_DATE).order_by(
                "-created"
            )[: self.MAX_SIZE]
            cache.set("recently_added", recently_added)

        # get highly rated courses
        highly_rated = cache.get("highly_rated")
        if not highly_rated:
            self.MAX_SIZE = 9
            highly_rated = (
                all_courses.annotate(num_ratings=Count("ratings"))
                .exclude(num_ratings__lt=1)
                .order_by("-num_ratings")[: self.MAX_SIZE]
            )
            cache.set("highly_rated", highly_rated)

        # get top instructors
        top_instructors = cache.get("top_instructors")
        if not top_instructors:
            top_instructors = (
                get_user_model()
                .objects.filter(is_instructor=True)
                .annotate(
                    total_courses=Count("courses_created"),
                    total_students=Sum("courses_created__students"),
                )
                .filter(total_students__gt=0)
                .order_by("-total_students")
            )
            print(top_instructors)
            print([s.total_students for s in top_instructors])

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f"subject_{subject.id}_courses"
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get("all_courses")
            if not courses:
                courses = all_courses
                cache.set("all_courses", courses)

        return self.render_to_response(
            {
                "subjects": subjects,
                "subject": subject,
                "courses": courses,
                "popular_courses": popular_courses,
                "recently_added": recently_added,
                "highly_rated": highly_rated,
                "top_instructors": top_instructors,
                "style": "index",
            }
        )


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course/details2.html"
    has_added_to_wishlist = []

    # render a form for user to add to cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user:
            pass
        # context["enroll_form"] = CourseEnrollForm(initial={"course": self.object})
        course_obj = self.object.id
        course = Course.objects.get(id=course_obj)

        if self.request.user.is_authenticated:
            self.has_added_to_wishlist = WishList.objects.filter(
                user=self.request.user, course=course
            ).exists()

        r = Recommender()
        recommended_courses = r.suggest_courses_for([course], 4)
        context["recommended_courses"] = recommended_courses
        context["style"] = "detail"  # load specific css
        context["has_added_to_wishlist"] = self.has_added_to_wishlist
        return context


class RatingView(TemplateResponseMixin, View):
    template_name = "courses/course/ratings.html"

    def dispatch(self, request, pk, *args, **kwargs):
        self.course = get_object_or_404(Course, id=pk)
        return super().dispatch(request, pk, *args, **kwargs)

    def post(self, request, *rags, **kwargs):
        rating_value = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        rating, created = Rating.objects.update_or_create(
            course=self.course,
            user=request.user,
            defaults={"rating": rating_value, "comment": comment},
        )
        if created:
            messages.success(request, "Thanks for your feedback")
            return redirect("")


def quizpage(request, course_id):

    course = Course.objects.filter(id=course_id).first()

    quiz = Quiz.objects.filter(course=course).order_by("created_at")

    return render(
        request,
        "quiz/list_quiz.html",
        {
            "quizzes": quiz,
            "course": course,
            "style": "quiz_list",
        },
    )


class QuizPage(TemplateResponseMixin, View):
    template_name = "quiz/list_quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "list_quizzes"
        return context

    def dispatch(self, request, course_id):
        self.course = get_object_or_404(Course, id=course_id)
        return super().dispatch(request, course_id)

    def get(self, request, course_id):
        quizzes = Quiz.objects.filter(course=self.course).order_by("created_at")

        return self.render_to_response(
            {
                "quizzes": quizzes,
                "course": self.course,
            }
        )


class QuizPageDetail(TemplateResponseMixin, View):
    template_name = "quiz/quizpage.html"

    def get(self, request, course_id, quiz_id, quiz_slug):
        course = Course.objects.filter(id=course_id).first()
        quiz = Quiz.objects.filter(id=quiz_id, course=course).first()
        return self.render_to_response(
            {
                "quiz": quiz,
                "style": "quiz_questions",
            }
        )


class QuizPageRender(TemplateResponseMixin, View):
    template_name = "quiz/quiz.html"

    def get(self, request, course_id, quiz_id, quiz_slug):
        course = Course.objects.filter(id=course_id).first()

        quiz = Quiz.objects.filter(id=quiz_id, course=course).first()

        return self.render_to_response(
            {
                "quiz": quiz,
                "style": "quiz_questions",
            }
        )


class QuizResultPage(TemplateResponseMixin, View):
    template_name = "quiz/quizresult.html"

    def get(self, request, quiz_id, quiz_slug):
        # course = Course.objects.filter(id=course_id).first()
        quiz = Quiz.objects.filter(id=quiz_id).first()
        return self.render_to_response(
            {
                "quiz": quiz,
                "style": "quiz_questions",
            }
        )


def course_search(request):
    query = None
    results = []
    similarity = []

    if "query" in request.GET:
        query = request.GET.get("query")

        # similarity search
        similarity = (
            Course.objects.annotate(
                similarity=TrigramSimilarity("title", query),
            )
            .filter(similarity__gte=0.1)
            .order_by("-similarity")
        )

        search_vector = (
            SearchVector("title", weight="A")
            + SearchVector("overview", weight="B")
            + SearchVector("course_description", weight="C")
        )
        search_query = SearchQuery(query)

        results = Course.objects.annotate(
            search=search_query, rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.3)

        # remove courses from similarity that appear in results
        filtered_similarity = similarity.exclude(title__in=[r.title for r in results])

    return render(
        request,
        "courses/search.html",
        {
            "query": query,
            "results": results,
            "similar": filtered_similarity,
            "style": "search",
        },
    )
