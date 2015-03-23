from django.conf.urls import patterns, include, url
from django.contrib import admin

import pgameapp.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin_site.urls)),
    url(r'', include('pgameapp.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/signup/', pgameapp.views.SignupView.as_view(), name="account_signup"),
    url(r'^accounts/', include("account.urls")),


)



