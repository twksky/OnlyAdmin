from django.conf.urls import url
from odmin import views


urlpatterns = [
    url(r'^$', views.index, name='odmin.index'),
    url(r'^example$', views.example, name='odmin.example'),
    url(r'^pages/create$', views.create, name='odmin.pages.create'),
    url(r'^pages/(?P<page_id>[0-9]+)/edit$', views.edit, name='odmin.pages.edit'),
    url(r'^pages$', views.index, name='odmin.pages'),
    url(r'^login$', views.login, name='odmin.login'),
    url(r'^logout$', views.logout, name='odmin.logout'),
]
