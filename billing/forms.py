from django import forms


class StripeTokenForm(forms.Form):
    stripe_token = forms.CharField()
