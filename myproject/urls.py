
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'practica2.views.view_info'),
    url(r'^(\d+)', 'practica2.views.content'),
    url(r'^(.*)', 'practica2.views.msg_error'),
]
