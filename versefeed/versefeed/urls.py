from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin
from quiz import views, versefeed_import
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'versefeed.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^import_db/$', versefeed_import.get_qn), 
    url(r'^quiz/$', views.quiz_home),
    url(r'^get_theme/$', views.get_theme),
    url(r'^themed_quiz/$', views.themed_quiz),
     url(r'^qn/$', views.qn), 
    url(r'^quiz_score/$', views.quiz_score),

)

urlpatterns += staticfiles_urlpatterns()
