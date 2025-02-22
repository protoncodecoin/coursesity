import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from courses.models import Course, Subject


from .models import InstructorProfile, Profile
from .tokens import generate_token
from . import tasks


logger = logging.getLogger(__name__)


# Create your views here.
class UserLoginView(TemplateResponseMixin, View):
    template_name = "users/account/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "login"
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response({"style": "login"})

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")

        # authenticate user
        user = authenticate(request, email=email, password=password)

        if user and user.is_active:
            login(request, user)

            if user.is_instructor:
                return redirect("manage_course_list")
            return redirect("student_course_list")

        messages.error(request, "Invalid credentials provided")
        return redirect("login")


class UserRegisterView(TemplateResponseMixin, View):
    template_name = "users/account/registration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "signup"
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response({"style": "signup"})

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        is_instructor = request.POST.get("is_instructor")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # validate email
        try:
            existing_user = get_user_model().objects.get(email=email)

            if existing_user.is_active:
                messages.error(request, "Email is already registered")
                return redirect("user_registration")
            else:
                # account verification wasn't complete
                existing_user.delete()
                messages.error(
                    request,
                    "Account verification wasn't completed for this account\n\nPlease re-sign up again.",
                )
                return redirect("user_registration")
        except Exception as e:
            logger.error(f"🥶🥶🥶 Exception from user registration {e}")

        # validate password
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("user_registration")

        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("user_registration")

        # create user
        try:
            myuser = get_user_model().objects.create_user(
                email=email, password=password1
            )
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.is_instructor = True if is_instructor else False
            myuser.is_active = False

            if is_instructor is not None:
                instructor_group = Group.objects.get(name="Instructors")
                myuser.groups.add(instructor_group)

            myuser.save()

        except Exception as e:
            messages.error(
                request,
                "Sorry something happened. Couldn't create account. Try again {0}".format(
                    e
                ),
            )
            return redirect("user_registration")

        # launch asynchronous task
        current_site = get_current_site(request)

        # logger.info(f"The new user is: {myuser.id}")

        tasks.send_welcome_email.delay(myuser.id)
        tasks.send_activation_email.delay(myuser.id, current_site.domain)

        messages.success(
            request,
            "Your account has been created successfully!\nPlease check your email to confirm your email address and activate your account.",
        )
        return redirect("login")


def activate_account(request, uidb64, token):
    """
    Activate the user account when verification email is clicked
    """
    user_obj = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = user_obj.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_obj.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()

        # create user profile
        if myuser.is_instructor:
            InstructorProfile.objects.create(user=myuser)
        else:
            Profile.objects.create(user=myuser)

        # login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect("login")
    else:
        return render(request, "registration/activation_failed.html")


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter()


def showProfile(request, user_id, user_slug):
    User = get_user_model()
    user_obj = get_object_or_404(User, id=user_id)
    # MAX_SIZE: int = 6

    if request.method == "POST":
        pass
    if user_obj.is_instructor:
        profile = InstructorProfile.objects.filter(user=user_obj).first()
        courses_created = Course.objects.filter(owner=user_obj)
        return render(
            request,
            "profile/instructor.html",
            {
                "style": "instructor",
                "profile": profile,
                "instructor": user_obj,
                "courses": courses_created,
            },
        )
    profile = Profile.objects.filter(user=user_obj).first()
    courses_completed = user_obj.courses_joined.filter(has_completed=True)
    student_interest = Subject.objects.filter(id=profile.field_of_study).first()
    return render(
        request,
        "profile/student.html",
        {
            "style": "student",
            "student": user_obj,
            "profile": profile,
            "courses_completed": courses_completed,
            "student_interest": student_interest,
        },
    )


def update_student_profile(request):
    if request.method == "POST":
        data = request.POST
        user = request.user
        profile_image = request.FILES.get("photo")

        print("File received in request.FILES:", profile_image)  # Debugging print

        user_obj = get_object_or_404(get_user_model(), id=user.id)
        profile_obj = Profile.objects.filter(user=user).first()

        # Update fields based on form data
        if data.get("interest"):
            profile_obj.field_of_study = data["interest"]
        if data.get("linkedIn"):
            user_obj.linkedIn = data["linkedIn"]
        if data.get("x"):
            user_obj.x = data["x"]

        # Update profile image if provided
        if profile_image:
            profile_obj.photo = profile_image
            print("Saving image:", profile_image)  # Debugging print

        # Save changes
        user_obj.save()
        profile_obj.save()

        messages.success(request, "Profile updated successfully")

    return render(
        request,
        "users/account/profile_update/student_profile.html",
        {"style": "update"},
    )


def update_instructor_profile(request):
    if request.method == "POST":
        data = request.POST
        user = request.user

        user_obj = get_object_or_404(get_user_model(), id=user.id)
        profile_obj = InstructorProfile.objects.filter(user=user_obj).first()
        print(profile_obj, user_obj.id, "------------------")

        profile_image = request.FILES.get("image")

        if request.POST.get("linkedIn") != "":
            user_obj.linkedIn = data["linkedIn"]
        if request.POST.get("website") != "":
            user_obj.website = data["website"]
        if request.POST.get("x") != "":
            user_obj.x = data["x"]
        if request.POST.get("about") != "":
            profile_obj.biography = data["about"]
        if request.POST.get("work") != "":
            profile_obj.institution = data["work"]
        if request.POST.get("experience") != "":
            profile_obj.years_of_experience = data["experience"]

        if profile_image:
            user_obj.photo = profile_image

        user_obj.save()
        profile_obj.save()

        messages.success(request, "profile updated successfully")
        # return redirect(f"show_profile/{user_obj.id}/{user_obj.slug}/")
    return render(
        request,
        "users/account/profile_update/instructor_profile.html",
        {
            "style": "update",
        },
    )
