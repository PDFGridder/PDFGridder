from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from plans.models import PlanPricing
from registration.signals import user_activated
from users.models import Profile

import stripe

from billing.tasks import (
    create_stripe_customer, update_stripe_customer, delete_stripe_customer,
    delete_stripe_plan, save_stripe_plan
)


stripe.api_key = settings.STRIPE_API_KEY


@receiver(pre_delete, sender=PlanPricing)
def delete_plan_pricing(sender, instance, **kwargs):
    plan_id = "%d-%d" % (instance.plan.pk, instance.pricing.pk)
    delete_stripe_plan.delay(plan_id)


@receiver(post_save, sender=PlanPricing)
def save_plan_pricing(sender, instance, created, **kwargs):
    save_stripe_plan(instance.pk)


@receiver(user_activated)
def create_customer(sender, user, **kwargs):
    Profile.objects.get_or_create(user=user)
    create_stripe_customer.delay(user.pk)


@receiver(post_save, sender=User)
def update_customer(sender, instance, created, **kwargs):
    if not created and instance.is_active:
        Profile.objects.get_or_create(user=instance)
        update_stripe_customer.delay(instance.pk)


@receiver(pre_delete, sender=Profile)
def delete_customer(sender, instance, **kwargs):
    customer_id = instance.stripe_customer_id
    delete_stripe_customer.delay(customer_id)
