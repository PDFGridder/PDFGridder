from django.conf.urls import include, url

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from tastypie.api import Api
from gridder.api import GridResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from billing.views import StripePaymentView
from users.forms import ProfileForm


v1_api = Api(api_name='v1')
v1_api.register(GridResource())

urlpatterns = [
    # Example:
    # (r'^website/', include('website.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/profile/', RedirectView.as_view(url='/', permanent=False)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^billing/', include('billing.urls')),
    url(r'^social_auth/', include('social_auth.urls')),
    url(r'^social_auth/email/', 'users.views.ask_email', name="social_auth_ask_email"),
    url(r'^plans/payments/(?P<pk>\d+)/$', StripePaymentView.as_view(), name='stripe_payment'),
    url(r'^plans/', include('plans.urls')),
    url(r'^profiles/edit/$', 'profiles.views.edit_profile', {'form_class': ProfileForm},
                           name='profiles_edit_profile'),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^profiles/avatar/', include('avatar.urls')),
    url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':  settings.MEDIA_ROOT}),

    url(r'^gridder/grids/(?P<object_id>\d+)/inx/$', 'gridder.views.inx', name="grid_export_inx"),
    url(r'^gridder/grids/(?P<object_id>\d+)/idml/$', 'gridder.views.idml', name="grid_export_idml"),
    url(r'^gridder/grids/(?P<object_id>\d+)/css/$', 'gridder.views.compass', name="grid_export_css"),
    url(r'^gridder/grids/(?P<object_id>\d+)/$', 'gridder.views.edit_grid', name="edit_grid"),
    url(r'^gridder/_=_$', 'gridder.views.grid', name="facebook_home"),
    url(r'^gridder/$', 'gridder.views.grid', name="home"),

    url(r'^users/(?P<username>.+)/faves/$', 'gridder.views.user_faves', name="user_faves"),
    url(r'^users/(?P<username>.+)/recents/$', 'gridder.views.user_recents', name="user_recents"),

    url('404', TemplateView.as_view(template_name='404.html'), name="404"),
    url('500', TemplateView.as_view(template_name='500.html'), name="500"),
    url(r'^make_grid/$', 'gridder.views.grid_ajax', name="grid_ajax"),
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', RedirectView.as_view(url='/gridder/', permanent=True)),
]

urlpatterns += staticfiles_urlpatterns()
