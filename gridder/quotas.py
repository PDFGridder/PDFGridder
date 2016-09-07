from django.conf import settings
from datetime import datetime
from django.core.exceptions import ValidationError

from .models import Grid
from plans import validators


class MaxGridsValidator(validators.ModelCountValidator):
    code = 'MAX_GRIDS_COUNT'
    model = Grid

    def get_queryset(self, user, request):
        if datetime.now() < settings.PLANS_START_DATE:
            return self.model.objects.none()

        if user.is_anonymous():
            return self.model.objects.filter(session_key=request.session.session_key)
        return self.model.objects.filter(user=user)

    def __call__(self, user, quota_dict=None, **kwargs):
        quota = self.get_quota_value(user, quota_dict)
        request = kwargs.get('request')
        total_count = self.get_queryset(user, request).count() + kwargs.get('add', 0)
        if not quota is None and total_count > quota:
            raise ValidationError(self.get_error_message(quota))


max_grids_validator = MaxGridsValidator()
