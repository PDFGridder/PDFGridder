from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from avatar.models import Avatar
from django_countries.fields import CountryField

from avatar.models import avatar_file_path


class Profile(models.Model):
    """(Profile description)"""
    user = models.OneToOneField('auth.User')
    upload_avatar = models.ImageField(max_length=1024, upload_to=avatar_file_path, blank=True, null=True)
    full_name = models.CharField(blank=True, max_length=200)
    bio = models.CharField(blank=True, max_length=500)
    city = models.CharField(blank=True, max_length=100)
    country = CountryField(blank=True)
    stripe_customer_id = models.CharField(null=True, blank=True, max_length=255, db_index=True)

    def __unicode__(self):
        return u"Profile for user %s" % self.user

    def save(self, *args, **kwargs):
        if self.upload_avatar and self.upload_avatar != self.avatar.avatar:
            Avatar.objects.create(
                user=self.user,
                avatar=self.upload_avatar,
                primary=True
            )
        return super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

    @property
    def avatar(self):
        try:
            return self.user.avatar_set.get(primary=True)
        except ObjectDoesNotExist:
            return None
