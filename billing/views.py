# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View
from django.views.generic.edit import DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin

import stripe
from plans.models import Order

from .models import Card
from .forms import StripeTokenForm

from billing.tasks import delete_stripe_card, update_stripe_card
stripe.api_key = settings.STRIPE_API_KEY


class StripePaymentView(SingleObjectMixin, View):
    model = Order

    def get_success_url(self):
        return self.object.get_absolute_url()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StripePaymentView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # get the credit card details submitted by the form
        token = request.POST['stripe_token']

        order = self.get_object()

        customer = stripe.Customer.retrieve(request.user.profile.stripe_customer_id)
        customer.card = token
        try:
            customer.subscriptions.create(plan="%d-%d" % (order.plan.pk, order.pricing.pk))
            customer.save()
        except stripe.error.CardError as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('order_payment_failure', kwargs={'pk': order.pk}))
        else:
            messages.success(request, 'Payment Successful.')
            order.complete_order()
            return HttpResponseRedirect(reverse('order_payment_success', kwargs={'pk': order.pk}))


class CardDetail(DetailView):
    model = Card

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CardDetail, self).dispatch(*args, **kwargs)

    def get_object(self):
        return self.model.objects.get(user=self.request.user)


class CardCreateEdit(FormView):
    form_class = StripeTokenForm
    template_name = 'billing/card_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CardCreateEdit, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('profiles_profile_detail', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        token = form.cleaned_data['stripe_token']
        customer_id = self.request.user.profile.stripe_customer_id
        update_stripe_card(customer_id, token)

        return super(CardCreateEdit, self).form_valid(form)


class CardDelete(DeleteView):
    model = Card

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CardDelete, self).dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user.card

    def get_success_url(self):
        return reverse('profiles_profile_detail', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        card = self.get_object()
        delete_stripe_card.delay(card.pk)
        return super(CardDelete, self).form_valid(form)
