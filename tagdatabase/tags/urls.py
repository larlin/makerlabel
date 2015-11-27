from django.conf.urls import patterns, url

from tags import views

urlpatterns = patterns('',
    url(r'^$', views.MemberListView.as_view(), name='main'),
    url(r'^add/$', views.Add.as_view(), name='add'),
    url(r'^members/$', views.MemberListView.as_view(), name='member_list'),
    url(r'^tags/$', views.TagListView.as_view(), name='tag_list'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='details'),
    url(r'^(?P<pk>\d+)/view/$', views.DetailView.as_view(), name='details_long'),
    url(r'^(?P<pk>\d+)/delete/$', views.Delete.as_view(), name='delete'),
    url(r'^(?P<tag_id>\d+)/download/$', views.download, name='download'),
    url(r'^(?P<tag_id>\d+)/print/$', views.print_pdf, name='print_pdf'),
)

