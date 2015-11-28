from django.conf.urls import patterns, url

from tags import views

urlpatterns = patterns('',
    url(r'^$', views.MainView.as_view(), name='main'),
    # Member views
    url(r'^members/$', views.MemberListView.as_view(), name='member_list'),
    url(r'^members/(?P<pk>\d+)/$', views.MemberDetailView.as_view(), name='member_details'),
    # Machine tag view
    url(r'^machines/(?P<pk>\d+)/$', views.MachineTagDetailView.as_view(), name='machine_tag_details'),
    url(r'^machines/add/$', views.MachineTagAdd.as_view(), name='machine_tag_add'),
    url(r'^machines/add/(?P<contact>\d+)$', views.MachineTagAdd.as_view(), name='machine_tag_add_as'),
    # Comment views
    url(r'^machines/(?P<machine>\d+)/comment$', views.CommentAdd.as_view(), name='machine_tag_comment_to'),
    url(r'^machines/comment$', views.CommentAdd.as_view(), name='machine_tag_comment'),
    # User tag views
    url(r'^tags/$', views.ListView.as_view(), name='tag_list'),
    url(r'^add/$', views.Add.as_view(), name='add'),
    url(r'^add/(?P<member_id>\d+)$', views.Add.as_view(), name='add_as'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='details'),
    url(r'^(?P<pk>\d+)/view/$', views.DetailView.as_view(), name='details_long'),
    url(r'^(?P<pk>\d+)/delete/$', views.Delete.as_view(), name='delete'),
    url(r'^(?P<tag_id>\d+)/download/$', views.download, name='download'),
    url(r'^(?P<tag_id>\d+)/print/$', views.print_pdf, name='print_pdf'),
)

