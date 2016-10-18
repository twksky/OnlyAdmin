from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect, render_to_response

from odmin.utils import admin_only, Pager
from odmin.models import Page
from odmin.forms import PageForm


@admin_only
def example(request):
    messages.add_message(request, messages.INFO, 'Hello world.')
    messages.add_message(request, messages.ERROR, 'Hello world.')
    messages.add_message(request, messages.SUCCESS, 'Hello world.')
    return render(request, 'odmin/example.html')


@admin_only
def index(request):
    return render(request, 'odmin/index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'odmin/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password, type=1)
        if not user or not user.is_staff:
            message = '用户名或密码错误'
            return render(request, 'odmin/login.html', context={
                "message": message
            })
        django_login(request, user)
        return redirect('odmin.index')


def logout(request):
    django_logout(request)
    return redirect('odmin.login')


def pages(request, page_id):
    page = Page.objects.get(pk=page_id)
    return render_to_response('odmin/page.html', context={
        "page": page
    })


@admin_only
def create(request):
    if request.method == 'POST':
        # Form valid and post
        form = PageForm(request.POST)
        if form.is_valid():
            Page.objects.create(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            messages.add_message(request, messages.SUCCESS, '增加成功')
            return redirect('odmin.pages')

        messages.add_message(request, messages.ERROR, '参数错误')

    return render(request, 'odmin/pages/edit.html')


@admin_only
def edit(request, page_id):

    page = Page.objects.get(pk=page_id)

    if request.method == 'POST':
        # Form valid and post
        form = PageForm(request.POST)
        if form.is_valid():
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.save()
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect('odmin.pages')

        messages.add_message(request, messages.ERROR, '参数错误')

    return render(request, 'odmin/pages/edit.html', context={
        "page": page
    })


@admin_only
def index(request):
    query = Page.objects.all()

    pager = Pager.from_request(query, request)
    return render(request, 'odmin/pages/index.html', context={
        "pager": pager
    })
