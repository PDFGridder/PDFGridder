from django.core.exceptions import ValidationError

import json

from tastypie.exceptions import Unauthorized, ImmediateHttpResponse
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization

from .models import Grid
from billing.utils import validate_plan


class GridAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        if object is not None:
            if object.user is None:
                return True
            if object.user is not None and request.user != object.user:
                return False
        return super(GridAuthorization, self).is_authorized(request, object)

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        if bundle.request.user.is_authenticated():
            return object_list.filter(user=bundle.request.user)

        return object_list.none()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return True

    def create_detail(self, object_list, bundle):

        try:
            validate_plan(bundle.request.user, add=1, request=bundle.request)
        except ValidationError as e:
            raise Unauthorized(' '.join(e.messages))
        return True

    def create_list(self, object_list, bundle):
        return object_list

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def delete_list(self, object_list, bundle):
        return self.update_list(object_list, bundle)

    def update_detail(self, object_list, bundle):
        return self.read_detail(object_list, bundle)

    def delete_detail(self, object_list, bundle):
        return self.update_detail(object_list, bundle)


class GridResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Grid.objects.all()
        resource_name = 'grids'
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = GridAuthorization()
        fields = (
            'id',
            'resource_uri',
            'baseline', 'baseline_unit',
            'baseine_color', 'baseline_opacity',
            'columns',
            'columns_color', 'columns_opacity',
            'columns_gutter', 'columns_gutter_unit',
            'name', 'description', 'summary',
            'created',
            'edit_url',
            'grid',
            'hash',
            'height', 'height_unit',
            'width', 'width_unit',
            'is_spread',
            'margin_botton', 'margin_bottom_unit',
            'margin_top', 'margin_top_unit',
            'margin_left', 'margin_left_unit',
            'margin_right', 'margin_right_unit',
            'star',
            'user_id',
        )
        filtering = {
            'star': ['exact'],
            'user': ALL
        }

    def obj_create(self, bundle, **kwargs):
        if bundle.request.user is not None:
            bundle.data['user_id'] = bundle.request.user.id
        bundle.data['session_key'] = bundle.request.session.session_key
        return super(GridResource, self).obj_create(bundle, **kwargs)

    def hydrate(self, bundle):
        if 'user_id' in bundle.data:
            bundle.obj.user_id = bundle.data['user_id']
        bundle.obj.session_key = bundle.request.session.session_key
        return bundle

    def dehydrate(self, bundle):
        if bundle.obj.user is not None:
            bundle.data['user_id'] = bundle.obj.user.id
        bundle.data['summary'] = bundle.obj.summary()
        bundle.data['edit_url'] = bundle.obj.get_edit_url()
        return bundle

    def unauthorized_result(self, exception):
        """Override tastypie method to return a reasonable error response."""
        raise ImmediateHttpResponse(
            response=HttpUnauthorized(
                json.dumps({'error': exception.message}),
                content_type='application/json'
            )
        )

