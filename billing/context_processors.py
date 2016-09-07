from django.conf import settings


def stripe_publishable_key(request):
    return {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY}
