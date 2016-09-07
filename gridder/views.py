# Create your views here.
import json
from zipfile import ZIP_DEFLATED

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.defaultfilters import date
from django.shortcuts import get_object_or_404

from django_zipfile import TemplateZipFile
import envoy

from .forms import GridForm
from .models import Grid


def grid_ajax(request):
    if request.method == 'POST':
        form = GridForm(request.POST, request=request)
        if form.is_valid():
            g = form.save(commit=False)
            if request.user.is_authenticated():
                g.user = request.user
            g.save()
            form.save_m2m()
            c = {
                'id': g.id,
                'name': g.__unicode__(),
                'summary': g.summary(),
                'url': g.get_params_url(),
                'created_human': date(g.created, "F, jS Y"),
                'download': g.get_absolute_url()
            }
            return HttpResponse(json.dumps(c), content_type='application/json')
        else:
            return HttpResponseBadRequest
    else:
        return HttpResponseNotAllowed(['POST'])


def grid(request):
    c = {}
    if request.method == 'POST':
        form = GridForm(request.POST, request=request)
        if form.is_valid():
            g = form.save(commit=False)
            if request.user.is_authenticated():
                g.user = request.user
            g.save()
            form.save_m2m()
            return HttpResponseRedirect(g.get_absolute_url())
        else:
            for k, v in request.POST.items():
                if k in form.fields:
                    form.fields[k].initial = v
    else:
        form = GridForm(request=request)

        for k, v in request.GET.items():
            if k in form.fields:
                form.fields[k].initial = v

    c.update({'form': form})

    if request.user.is_authenticated():
        grid_id = int(request.GET.get('id', False))
        c.update({'grid_id': grid_id})

        recent_list = request.user.grid_set.all()
        if len(recent_list):
            try:
                recents_page = int(request.GET.get('recents_page', 1))
            except ValueError:
                recents_page = 1
            recents_paginator = Paginator(recent_list, 10)
            recents = recents_paginator.page(recents_page)
            c.update({'recents': recents})

    return render_to_response('gridder/grid_form.html',
        c,
        context_instance=RequestContext(request)
    )


def inx(request, object_id):
    g = get_object_or_404(Grid, pk=object_id)
    ctx = {
        'object': g
    }

    response = render_to_response(
        'gridder/indesign.inx',
        ctx,
        context_instance=RequestContext(request),
        content_type='application/octet-stream'
    )
    response['Content-Disposition'] = 'attachment; filename=' + slugify(g.name) + '.inx'
    return response


def idml(request, object_id):
    g = get_object_or_404(Grid, pk=object_id)
    c = {
        'object': g
    }
    response = HttpResponse(content_type='application/vnd.adobe.indesign-idml-package')
    response['Content-Disposition'] = 'attachment; filename=' + slugify(g.name) + '.idml'
    idml_container = TemplateZipFile(response, mode='w', compression=ZIP_DEFLATED, template_root='gridder/idml/')

    idml_container.write_template('mimetype')
    idml_container.write_template('designmap.xml')
    idml_container.write_template('META-INF/container.xml')
    idml_container.write_template('Resources/Preferences.xml', context=c)
    idml_container.write_template('Spreads/Spread_uba.xml', context=c)
    idml_container.write_template('MasterSpreads/MasterSpread_uc1.xml', context=c)

    idml_container.close()
    return response


def compass(request, object_id):
    g = get_object_or_404(Grid, pk=object_id)
    c = {
        'object': g
    }

    scss = render_to_string(['gridder/compass/compass.scss'],
        c,
        context_instance=RequestContext(request)
    )
    r = envoy.run('/usr/local/bin/scss -s --trace --compass', data=scss, timeout=2)
    if not r.std_err:
        response = HttpResponse(r.std_out, content_type='text/css')
        response['Content-Disposition'] = 'attachment; filename=' + slugify(g.name) + '.css'
        return response
    else:
        raise Exception(r.std_err)


@login_required
def edit_grid(request, object_id):
    g = get_object_or_404(Grid, pk=object_id)

    if g.user == request.user:
        c = {}
        if request.method == 'POST':
            form = GridForm(request.POST, instance=g, request=request)
            if form.is_valid():
                form.save()
            else:
                for k, v in request.POST.items():
                    if k in form.fields:
                        form.fields[k].initial = v
        else:
            form = GridForm(instance=g, request=request)

        c.update({'form': form, 'object': g})

        recent_list = request.user.grid_set.all()
        if len(recent_list):
            try:
                recents_page = int(request.GET.get('recents_page', 1))
            except ValueError:
                recents_page = 1
            recents_paginator = Paginator(recent_list, 10)
            recents = recents_paginator.page(recents_page)
            c.update({'recents': recents})

        return render_to_response('gridder/grid_form.html',
            c,
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseForbidden('Not yours.')


@login_required
def user_faves(request, username):
    if request.method == 'GET':
        if request.user.username == username:
            u = get_object_or_404(User, username=username)
            fave_list = u.grid_set.filter(star=True)

            return render_to_response('gridder/faves.json', {
                'faves': fave_list
                },
                context_instance=RequestContext(request),
                content_type='application/json'
            )
        else:
            return HttpResponseForbidden('No perusing')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required
def user_recents(request, username):
    if request.method == 'GET':
        if request.user.username == username:
            try:
                per_page = int(request.GET.get('perpage', 10))
            except ValueError:
                per_page = 10

            try:
                page = int(request.GET.get('page', 1))
            except ValueError:
                page = 1
            print page

            u = get_object_or_404(User, username=username)
            recent_list = u.grid_set.all()
            paginator = Paginator(recent_list, per_page)

            # If page request (9999) is out of range, deliver last page of results.
            try:
                recents = paginator.page(page)
            except (EmptyPage, InvalidPage):
                return HttpResponseBadRequest('Invalid page')

            return render_to_response('gridder/recents.json',
                {'recents': recents},
                context_instance=RequestContext(request),
                content_type='application/json'
            )
        else:
            return HttpResponseForbidden('No perusing')
    else:
        return HttpResponseNotAllowed(['POST'])
