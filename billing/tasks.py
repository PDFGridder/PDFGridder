from billing.models import Card
from pdfgridder import celery_app
from django.conf import settings
from django.contrib.auth.models import User

import stripe

stripe.api_key = settings.STRIPE_API_KEY


@celery_app.task(name='billing.tasks.create_stripe_customer')
def create_stripe_customer(user_id):
    user = User.objects.get(pk=user_id)

    customer = stripe.Customer.create(
        email=user.email,
        metadata={'user_pk': "%d" % user_id}
    )
    user.profile.stripe_customer_id = customer.id
    user.profile.save()


@celery_app.task(name='billing.tasks.update_stripe_customer')
def update_stripe_customer(user_id):
    user = User.objects.get(pk=user_id)
    customer_id = user.profile.stripe_customer_id
    customer = stripe.Customer.retrieve(customer_id)
    customer.email = user.email
    customer.save()


@celery_app.task(name='billing.tasks.delete_stripe_customer')
def delete_stripe_customer(customer_id):
    try:
        customer = stripe.Customer.retrieve(customer_id)
        customer.delete()
    except stripe.error.InvalidRequestError as e:
        if e.http_status != 404:
            raise


INTERVALS = {
    1: 'day',
    7: 'week',
    30: 'month',
    365: 'year',
}


@celery_app.task(name='billing.tasks.delete_stripe_plan')
def delete_stripe_plan(plan_id):
    try:
        plan = stripe.Plan.retrieve(plan_id)
        plan.delete()
    except stripe.error.InvalidRequestError as e:
        if e.http_status != 404:
            raise


@celery_app.task(name='billing.tasks.save_stripe_plan')
def save_stripe_plan(planpricing_id):
    from plans.models import PlanPricing

    instance = PlanPricing.objects.get(pk=planpricing_id)
    plan_id = "%d-%d" % (instance.plan.pk, instance.pricing.pk)
    plan_name = "%s %s" % (instance.plan.name, instance.pricing.name)
    plan_amount = int(instance.price * 100)
    plan_interval = INTERVALS[instance.pricing.period]
    plan_currency = settings.CURRENCY.lower()
    plan_trial = settings.PLAN_DEFAULT_GRACE_PERIOD

    delete_stripe_plan(plan_id)

    stripe.Plan.create(
        name=plan_name,
        amount=plan_amount,
        interval=plan_interval,
        currency=plan_currency,
        trial_period_days=plan_trial,
        id=plan_id
    )


@celery_app.task(name='billing.tasks.delete_stripe_card')
def delete_stripe_card(card_id):
    from billing.models import Card

    card = Card.objects.get(pk=card_id)
    customer = stripe.Customer.retrieve(card.user.profile.stripe_customer_id)
    customer.cards.retrieve(card=card.token).delete()
    card.delete()


@celery_app.task(name='billing.tasks.update_stripe_card')
def update_stripe_card(customer_id, token):
    user = User.objects.get(profile__stripe_customer_id=customer_id)
    try:
        old_card = user.card
    except Card.DoesNotExist:
        is_new = True
    else:
        is_new = False
    customer = stripe.Customer.retrieve(customer_id)

    if not is_new:
        customer.cards.retrieve(card=old_card.token).delete()
        old_card.delete()

    stripe_card = customer.cards.create(card=token)
    customer.default_card = stripe_card.id
    customer.save()

    Card.objects.create_from_stripe(
        user=user,
        stripe_card=stripe_card
    )
