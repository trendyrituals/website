from django.conf.urls import url
from .views import (

	login_view,
	registration,
	
	about,
	index
	
	)


urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^about/$', about, name='about'),
    url(r'^$', index, name='index'),
    ]