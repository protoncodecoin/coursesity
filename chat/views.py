from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from courses.models import Course


# Create your views here.
@login_required
def course_chat_room(request, course_id):
    try:
        # retrieve course with given id joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # user is not a student of the course or the course does not exists
        return HttpResponseForbidden()
    # retrieve chat history
    latest_messages = course.chat_messages.select_related("user").order_by("-id")[:50]
    latest_messages = reversed(latest_messages)

    return render(
        request,
        "chat/room2.html",
        {
            "course": course,
            "latest_messages": latest_messages,
            "style": "room",
        },
    )
