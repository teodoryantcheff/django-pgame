from django.conf.urls import patterns, include, url
from django.contrib import admin

from pgameapp.views import index
from pgameapp.views import accounts

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin_site.urls)),
    url(r'^$', index.IndexView.as_view(), name='index'),
    url(r'^game/', include('pgameapp.urls')),

    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/signup/', accounts.SignupView.as_view(), name="account_signup"),
    url(r'^accounts/', include("account.urls")),

    url(r'^news/', include('news.urls')),
)



