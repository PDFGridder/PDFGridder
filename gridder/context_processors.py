from django.conf import settings


def facebook_app_id(request):
    return {'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID}


def analytics(request):
    return {'GOOGLE_ANALYTICS_UA': settings.GOOGLE_ANALYTICS_UA}
