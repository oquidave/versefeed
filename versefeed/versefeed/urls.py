from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



from django.contrib import admin
from quiz import views, versefeed_import
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^import_db/$', versefeed_import.get_qn), #import quiz from legacy db to django models
    url(r'^quiz/$', views.quiz_home),
    #url(r'', views.quiz_home), #quiz home page, loads all the themes
    url(r'^get_theme/$', views.get_theme), #ajax request for details of clicked quiz
    url(r'^themed_quiz/$', views.themed_quiz), #start theme's quiz
    url(r'^qn/$', views.qn), #ajax request of quiz qns
    url(r'^quiz_score/$', views.quiz_score), #ajax request to load the final quiz score for particular quiz round
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^about/$', views.about),
    url(r'^contact/$', views.contact),

)

#social login 
urlpatterns += patterns('',
  url(r'', include('social_auth.urls')),
)

urlpatterns += staticfiles_urlpatterns()
