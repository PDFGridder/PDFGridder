from django.core.exceptions import ValidationError
from django.conf import settings
from plans.importer import import_name
from plans.models import Plan, UserPlan


def validate_plan(user, plan=None, **kwargs):
    if plan is None:
        if user.is_authenticated():
        # if plan is not given, the default is to use current plan of the user
            plan = user.userplan.plan
        else:
            plan = Plan.objects.get(default=True)

    quota_dict = plan.get_quota_dict()
    validators = getattr(settings, 'PLAN_VALIDATORS', {})
    errors = []
    for quota in quota_dict:
        if quota in validators:
            validator = import_name(validators[quota])
            try:
                validator(user, quota_dict, **kwargs)
            except ValidationError as e:
                errors.extend(e.messages)
    if len(errors):
        raise ValidationError(errors)
    return True
