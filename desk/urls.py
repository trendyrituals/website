from django.conf.urls import url
from .views import (
		home,
		add_course,
		coins,
		logout_view,
		search_course,
		user_course,
		user_course_view,
		ready_user,
		cost_view,
		delete_course,
		pay_success,
		pay_unsuccessful,	
	)


urlpatterns = [
	url(r'^unsuccessful/$', pay_unsuccessful, name='pay_unsuccessful'),
	url(r'^success/$', pay_success, name='pay_success'),
	url(r'^user_course/delete/(?P<id>\d+)/$', delete_course, name='delete_course'),
	url(r'^view_course/(?P<id>\d+)/$', cost_view, name='cost_view'),
	url(r'^ready_user/(?P<username>\w{0,50})/$', ready_user, name='ready_user_view'),
	url(r'^user_course/(?P<id>\d+)/$', user_course_view, name='user_course_view'),
	url(r'^user_course/$', user_course, name='user_course'),
	url(r'^search/$', search_course, name='search_course'),
    url(r'^logout/$', logout_view, name='logout_view'),
    url(r'^coins/$', coins, name='coins'),
    url(r'^add_course/$', add_course, name='add_course'),
    url(r'^$', home, name='home'),
    ]
