from django.conf.urls import patterns, url

from tags import views

urlpatterns = patterns('',
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^add/$', views.Add.as_view(), name='add'),
    url(r'^member/$', views.MemberListView.as_view(), name='details'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='details'),
    url(r'^(?P<pk>\d+)/view/$', views.DetailView.as_view(), name='details_long'),
    url(r'^(?P<pk>\d+)/delete/$', views.Delete.as_view(), name='delete'),
    url(r'^(?P<tag_id>\d+)/download/$', views.download, name='download'),
    url(r'^(?P<tag_id>\d+)/print/$', views.print_pdf, name='print_pdf'),
)

