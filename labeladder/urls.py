from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.enter_page, name='read_file'),
]