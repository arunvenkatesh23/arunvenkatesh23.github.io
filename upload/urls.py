from django.conf.urls import url
from . import views

app_name = 'upload'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_folder/$', views.create_folder, name='folder_add'),
    url(r'^(?P<folder_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<folder_id>[0-9]+)/file_add/$', views.create_file, name='file_add'),
    url(r'^files/(?P<filter_by>[a-zA_Z]+)/$', views.files, name='files'),
    url(r'^(?P<filter_by>[a-zA_Z]+)/$', views.folders, name='folders'),
    url(r'^(?P<folder_id>[0-9]+)/(?P<file_id>[0-9]+)/favorite_file/$', views.favorite_file, name='favorite_file'),
    url(r'^(?P<folder_id>[0-9]+)/update_folder/$', views.update_folder, name='folder_update'),
    url(r'^(?P<folder_id>[0-9]+)/delete_folder/$', views.delete_folder, name='folder_delete'),
    url(r'^(?P<folder_id>[0-9]+)/favorite_folder/$', views.favorite_folder, name='favorite_folder'),
    url(r'^(?P<folder_id>[0-9]+)/delete_file/(?P<file_id>[0-9]+)/$', views.delete_file, name='file_delete'),
    url(r'^delete_file/(?P<file_id>[0-9]+)/$', views.files_delete, name='files_delete'),
    url(r'profile_settings/$', views.profile_settings, name='profile'),
]
