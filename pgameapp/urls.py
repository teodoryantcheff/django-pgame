from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required as auth
from django.core.urlresolvers import reverse_lazy

from pgameapp.views import UserProfileView, CollectCoinsView, SellCoinsView, StoreView, ExchangeView, ReferralsView

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),

    url(r'^$', auth(UserProfileView.as_view()),
        name='user-profile'),

    url(r'^collect/$', auth(CollectCoinsView.as_view(success_url = reverse_lazy('user-profile'))),
        name='collect-coins'),

    url(r'^sell/$', auth(SellCoinsView.as_view(success_url = reverse_lazy('user-profile'))),
        name='sell-coins'),

    url(r'^store/$', auth(StoreView.as_view(success_url = reverse_lazy('store'))),
        name='store'),

    # url(r'^store2/$', auth(StoreView2.as_view()), name='store2'),
    # url(r'^buy/$', auth(BuyFormView.as_view(success_url = reverse_lazy('store'))), name='buy'),

    url(r'^exchange/$', auth(ExchangeView.as_view(success_url = reverse_lazy('user-profile'))),
        name='exchange'),

    url(r'^referrals/$', auth(ReferralsView.as_view()),
        name='referrals'),
)