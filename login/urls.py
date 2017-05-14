from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'login'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about us/$', views.about_us, name='about_us'),
    url(r'^services/$', views.services, name='services'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^activation/',views.activate, name='activation'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^admin/$', views.admin_login, name='admin_login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^(?P<user_id>[0-9]+)/personal_details/$', views.personal_details, name='personal_details'),
    url(r'^personal_details/update/$', views.personal_details_update, name='personal_details_update'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^delete_account/$', views.delete_account_page, name='delete_account_page'),
    url(r'^(?P<user_id>[0-9]+)/delete_account/$', views.delete_account, name='delete_account'),
]
urlpatterns += staticfiles_urlpatterns()
