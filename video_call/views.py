from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
from courses.models import Course

import uuid

# exprity time for instant meetings
TIMEOUT: timedelta = 1440


# Create your views here.
@login_required
def register_meeting(request):

    if request.method == "POST":
        meeting_name = request.POST.get("meeting_name")

        # generate meeting token and save it in the cache
        meeting_token = uuid.uuid4()

        unique_meeting = str(meeting_token) + f"_{meeting_name}"
        cache.set(str(meeting_token), unique_meeting, TIMEOUT)

        return redirect(f"/meeting/room/{unique_meeting}/")

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

        unique_key = meeting_id.split("_")[0]

        print(meeting_id, "this is the meeting id")

        # check to see if meeting id is in cache
        meeting_token = cache.get(str(unique_key))
        print("this is the token", meeting_token)

        if meeting_token:
            return redirect(f"/meeting/room/{meeting_id}/")

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
    unique_id = meeting_id.split("_")[0]
    meeting_token = cache.get(unique_id)

    if not meeting_token:
        return redirect("join_meeting")

    user = request.user
    # context =

    return render(
        request,
        "video_call/room.html",
        {
            "uid": user.id,
            "displayName": user.get_full_name(),
            "style": "meeting_room",
            "room_info": meeting_token,
        },
    )
