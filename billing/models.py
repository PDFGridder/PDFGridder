from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class CardManager(models.Manager):
    def create_from_stripe(self, user, stripe_card):
        return self.create(
            user=user,
            token=stripe_card.id,
            last4=stripe_card.last4,
            brand=stripe_card.brand,
            exp_month=stripe_card.exp_month,
            exp_year=stripe_card.exp_year,
        )


class Card(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=255, unique=True)
    last4 = models.CharField(max_length=4)
    brand = models.CharField(blank=True, null=True, max_length=100)
    exp_month = models.PositiveSmallIntegerField()
    exp_year = models.PositiveSmallIntegerField()

    objects = CardManager()

    def __unicode__(self):
        return '%s **** **** **** %s (exp: %02d/%d)' % (
            self.brand,
            self.last4,
            self.exp_month,
            self.exp_year
        )

    def get_absolute_url(self):
        return reverse('card_create')
