# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from users.forms import EmailForm


def ask_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            request.session['saved_email'] = form.cleaned_data['email']
            backend = request.session['partial_pipeline']['backend']
            return redirect('socialauth_complete', backend=backend)
    else:
        form = EmailForm()

    return render_to_response('social_auth/ask_email.html', {
        'form': form
    }, RequestContext(request))
