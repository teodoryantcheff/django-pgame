from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required as lr
from django.core.urlresolvers import reverse_lazy

from pgameapp.views import UserProfileView, CollectCoinsView, SellCoinsView, StoreView, ExchangeView, ReferralsView

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),

    url(r'^$', lr(UserProfileView.as_view()),
        name='user-profile'),

    url(r'^collect/$', lr(CollectCoinsView.as_view(success_url = reverse_lazy('user-profile'))),
        name='collect-coins'),

    url(r'^sell/$', lr(SellCoinsView.as_view(success_url = reverse_lazy('user-profile'))),
        name='sell-coins'),

    url(r'^store/$', lr(StoreView.as_view(success_url = reverse_lazy('store'))),
        name='store'),

    url(r'^exchange/$', lr(ExchangeView.as_view(success_url = reverse_lazy('user-profile'))),
        name='exchange'),

    url(r'^referrals/$', lr(ReferralsView.as_view()),
        name='referrals'),
)