from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from celery import shared_task

from courses.models import Course
from users.models import Meeting


@shared_task(bind=True)
def notify_meeting_participants(self, course_id: int, meeting_id: int):
    """
    Task to send email notificaion to participants of the meeting.
    """
    course_obj = Course.objects.filter(id=course_id).first()
    meeting_obj = Meeting.objects.filter(id=meeting_id).first()
    student_emails = [student.email for student in course_obj.students.all()]

    try:

        subject = f"Coursity: {course_obj.title}"
        message = f"{meeting_obj.meeting_name}\n\n{meeting_obj.about_message}.\n\n\nTime: {meeting_obj.sch_time} Date: {meeting_obj.sch_date}\n\nMeeting ID: {meeting_obj.meeting_token}"
        from_email = settings.EMAIL_HOST_USER

        sent_email = send_mail(
            subject, message, from_email, student_emails, fail_silently=True
        )
        return sent_email

    except Exception as e:
        # log exception rather
        # print(str(e))
        raise self.retry(exc=e, countdown=5)


@shared_task(bind=True)
def notify_meeting_creator(self, instructor_id: int, course_id: int, meeting_id: int):
    """
    Task to send meeting id to instructor
    """
    try:
        instructor = (
            get_user_model()
            .objects.filter(id=instructor_id, is_instructor=True)
            .first()
        )
        # course_obj = Course.objects.filter(id=course_id).first()
        meeting_obj = Meeting.objects.filter(id=meeting_id).first()
        subject = f"Meeting {meeting_obj.meeting_name}"
        message = f"Meeting ID: {meeting_obj.meeting_token}\n\nMeeting Time: {meeting_obj.sch_time}\n\nMeeting Date: {meeting_obj.sch_date}"
        from_email = settings.EMAIL_HOST_USER

        sent_mail = send_mail(
            subject, message, from_email, [instructor.email], fail_silently=True
        )
        return sent_mail

    except Exception as e:
        raise self.retry(self, exc=e, countdown=5)


# @shared_task
# def send_course_link(student_id: int, courses: list):
#     """
#     Send course success links to student on successful transaction
#     """
#     # generate course links
#     message = f"CONGRATULATIONS TAKING THE NEXT STEP IN YOUR ACADEMIC JOURNEY. WE ARE HERE ROOTING FOR YOU. KEEP PUSHING.\nBELOW IS THE LINK TO ACCESS YOUR COURSE"

#     for course_id in courses:
#         course_obj = Course.objects.filter(id=course_id).first()
#         msg = f"\n\nCourse Title: {course_obj.title}\nAccess Link: {course_obj.get_absolute_url()}"
#         message += msg

#     student = get_user_model().objects.filter(id=student_id).first()

#     try:

#         subject = f"ENROLLMENT SUCCESSFUL"
#         message = message
#         from_email = settings.EMAIL_HOST_USER

#         sent_email = send_mail(
#             subject, message, from_email, [student.email], fail_silently=False
#         )
#         return sent_email

#     except Exception as e:
#         # log exception rather
#         print(str(e))
