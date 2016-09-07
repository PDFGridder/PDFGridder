from django.conf import settings
from pdfgridder import celery_app

from mailchimp import chimpy


@celery_app.task(name='marketing.tasks.create_mailchimp_recipient')
def create_mailchimp_recipient(user_id):
    from django.contrib.auth.models import User

    user = User.objects.get(pk=user_id)
    conn = chimpy.Connection(settings.MAILCHIMP_API_KEY)

    if user.is_active and user.email:
        try:
            conn.list_subscribe(settings.MAILCHIMP_USERS_LIST_ID, user.email, {
                'EMAIL': user.email,
                'FNAME': user.first_name,
                'LNAME': user.last_name,
            }, double_optin=False)
        except chimpy.chimpy.ChimpyException:
            pass

@celery_app.task(name='marketing.tasks.delete_mailchimp_recipient')
def delete_mailchimp_recipient(email):
    conn = chimpy.Connection(settings.MAILCHIMP_API_KEY)

    try:
        conn.list_unsubscribe(settings.MAILCHIMP_USERS_LIST_ID, email, delete_member=True, send_goodbye=False, send_notify=False)
    except chimpy.chimpy.ChimpyException:
        pass
