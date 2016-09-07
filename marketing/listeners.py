from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from registration.signals import user_activated

from marketing.tasks import create_mailchimp_recipient, delete_mailchimp_recipient


def delete_mailchimp_email(sender, instance, **kwargs):
    if instance.pk:
        old_email = User.objects.get(pk=instance.pk).email
        delete_mailchimp_recipient.delay(old_email)


def create_mailchimp_email(sender, **kwargs):
    if 'user' in kwargs:
        instance = kwargs['user']
    elif 'instance' in kwargs:
        instance = kwargs['instance']
    if instance.is_active:
        create_mailchimp_recipient.delay(instance.pk)


user_activated.connect(create_mailchimp_email)
pre_delete.connect(delete_mailchimp_email, sender=User)
