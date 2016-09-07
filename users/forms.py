from django import forms
from honeypot.fields import Honeypot

from .models import Profile


class EmailForm(forms.Form):
    message = Honeypot()
    email = forms.EmailField()


class ProfileForm(forms.ModelForm):
    message = Honeypot()
    email = forms.EmailField(initial='dsad@dsa.com')

    class Meta:
        model = Profile
        fields = (
            'message',
            'upload_avatar',
            'full_name',
            'bio',
            'city',
            'country',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.initial['email'] = self.instance.user.email

    def save(self, commit=True):
        self.instance.user.email = self.cleaned_data['email']
        if commit:
            self.instance.user.save()
        super(ProfileForm, self).save(commit)
