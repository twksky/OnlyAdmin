import math
from urllib.parse import urlencode

from django.shortcuts import redirect
from functools import wraps


class AdminMenu(object):

    def __init__(self, name, view_name=None, icon_classes='fa-circle-o', sub_menus=None, description=None,
                 extra_view_names=None):
        self.extra_view_names = extra_view_names
        self.description = description
        self.sub_menus = sub_menus
        self.icon_classes = icon_classes
        self.view_name = view_name
        self.name = name

    def active(self, view_name):

        if view_name == self.view_name:
            return True

        if self.extra_view_names and view_name in self.extra_view_names:
            return True

        return False


class RootMenu(object):

    index_menu = AdminMenu('Dashboard', 'odmin.index', 'fa-dashboard', description='控制面板页面')

    init_menus = [
        index_menu,
        AdminMenu('富文本管理',
                  icon_classes='fa-safari',
                  sub_menus=[
                      AdminMenu('新页面', 'odmin.pages.create'),
                      AdminMenu('富文本列表', 'odmin.pages', extra_view_names=[
                          'odmin.pages.edit',
                      ]),
                  ]),
        AdminMenu('样例', 'odmin.example', 'fa-code',
                  description='这个是一个测试页面',
                  sub_menus=[
                  ]),
    ]

    def __init__(self, current_view_name):
        self.current_view_name = current_view_name
        self.current_menu = None
        self.parent_menu = None
        self.menus = []

        for menu in self.init_menus:
            self.add_menu(menu)

    def add_menu(self, menu):
        view_name = self.current_view_name
        if menu.active(view_name):
            self.current_menu = menu
        elif menu.sub_menus:
            for sub_menu in menu.sub_menus:
                if sub_menu.active(view_name):
                    self.current_menu = sub_menu
                    self.parent_menu = menu
                    break

        self.menus.append(menu)
        return self


class Pager(object):

    def __init__(self, query, page, size, params=None):
        self.count = query.count()

        start = (page - 1) * size
        end = start + size
        self.items = query[start: end]
        self.page = page
        self.size = size
        self.params = params

    @property
    def has_next(self):
        return self.count > self.page * self.size

    @property
    def has_next_two(self):
        return self.count > (self.page + 1) * self.size

    @property
    def last_page(self):
        return math.ceil(self.count / self.size)

    @classmethod
    def from_request(cls, query, request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 20))
        params = {k: v[0] for k, v in dict(request.GET).items()}

        if 'page' in params:
            params.pop('page')

        if 'size' in params:
            params.pop('size')

        params.update(size=size)
        return Pager(query, page, size, params)

    @property
    def url_params(self):
        return urlencode(self.params)


def admin_config(request):
    return {
        "ROOT_MENU": RootMenu(current_view_name=request.resolver_match.view_name)
    }


def admin_only(api_func):
    @wraps(api_func)
    def _warp(request, *args, **kwargs):
        if not request.user.id or not request.user.is_staff:
            return redirect('odmin.login')

        return api_func(request, *args, **kwargs)
    return _warp
