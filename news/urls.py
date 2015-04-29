from django.conf.urls import patterns, url
from news.views import NewsSummaryView, NewsDetailView

__author__ = 'Jailbreaker'


urlpatterns = patterns(
    "",
    #url(r"^list/$", NewsSummaryView.as_view(), name='news_summary_view'),
    url(r'^$', NewsSummaryView.as_view(), name='news_summary_view'),
    url(r'^(?P<pk>[0-9]+)/$', NewsDetailView.as_view(), name='news_detail_view'),
)