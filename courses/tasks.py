from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

from courses.models import Course
from users.models import Meeting


@shared_task
def notify_meeting_participants(course_id: int, meeting_id):
    course_obj = Course.objects.filter(id=course_id).first()
    meeting_obj = Meeting.objects.filter(id=meeting_id)
    student_emails = [student.email for student in course_obj.students.all()]

    try:

        subject = f"Coursity: {course_obj.title}"
        message = f"{meeting_obj.title}\n\n{meeting_obj.about_message}."
        from_email = settings.EMAIL_HOST_USER

        sent_email = send_mail(
            subject, message, from_email, student_emails, fail_silently=True
        )
        return sent_email

    except Exception as e:
        print(str(e))
