from django.conf.urls import patterns, url

from tags import views

urlpatterns = patterns('',
	url(r'^$', views.list, name='list'),
    url(r'^add/$', views.add, name='add'),
	url(r'^(?P<tag_id>\d+)/$', views.details, name='details'),
    url(r'^(?P<tag_id>\d+)/view/$', views.details, name='details_long'),
    url(r'^(?P<tag_id>\d+)/download/$', views.download, name='download'),
    url(r'^(?P<tag_id>\d+)/print/$', views.print_pdf, name='print_pdf'),
)

