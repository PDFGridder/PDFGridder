from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from social_auth.backends.pipeline.associate import associate_by_email as _associate_by_email
from social_auth.exceptions import AuthException


def ask_email(*args, **kwargs):
    if not kwargs['request'].session.get('saved_email') and kwargs.get('user') is None:
        url = reverse('social_auth_ask_email')
        return HttpResponseRedirect(url)
    return {}


def associate_by_email(details, *args, **kwargs):
    request = kwargs['request']
    if 'saved_email' in request.session:
        details['email'] = request.session['saved_email']
    try:
        return _associate_by_email(details, *args, **kwargs)
    except AuthException as error:
        messages.error(request, error.message)
        url = reverse('500')
        return HttpResponseRedirect(url)
