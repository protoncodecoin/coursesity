from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
import requests
from courses.models import Course
from users.models import Meeting

from . import token_generator

import uuid

# exprity time for instant meetings
TIMEOUT: timedelta = 1440


# Create your views here.
@login_required
def register_meeting(request):

    if request.method == "POST":
        meeting_name = request.POST.get("meeting_name")

        # generate meeting token and save
        # meeting_token = uuid.uuid4()
        meeting_token: str = token_generator.video_token_generator()

        new_meeting = Meeting.objects.create(
            host=request.user,
            course=None,
            meeting_name=meeting_name,
            meeting_token=meeting_token,
        )

        return redirect("meeting_room", new_meeting.meeting_token)

    return render(
        request,
        "video_call/lobby.html",
        {
            "style": "register_meeting",
        },
    )


@login_required
def join_meeting(request):
    if request.method == "POST":
        meeting_id = request.POST.get("meeting_id")

        # get meeting from db
        meeting_obj = Meeting.objects.filter(meeting_token=meeting_id).first()

        if meeting_obj:
            return redirect("meeting_room", meeting_obj.meeting_token)

        messages.error(request, "Invalid meeeting id")
        return redirect("join_meeting")

    return render(
        request,
        "video_call/join_meeting.html",
        {
            "style": "register_meeting",
        },
    )


@login_required
def meeting_room(request, meeting_id):
    user = request.user

    meeting_obj = Meeting.objects.filter(meeting_token=meeting_id).first()

    if not meeting_obj:
        return redirect("join_meeting")

    # set information in session
    # request.session["roomName"] = meeting_obj.meeting_name
    # request.session["uid"] = user.id
    # request.session["userName"] = user.get_full_name()

    # print(request.session.items())

    #  get token from the backend
    token = token_generator.buildRTCToken(
        channel_name=meeting_obj.meeting_name, uid=user.id
    )
    print(token)

    return render(
        request,
        "video_call/room.html",
        {
            "uid": user.id,
            "displayName": user.get_full_name(),
            "style": "meeting_room",
            "room_info": meeting_obj,
            "token": token,
        },
    )
