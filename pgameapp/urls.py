from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required as auth
from django.core.urlresolvers import reverse_lazy

from pgameapp.views import UserProfileView, CollectCoinsView, SellCoinsView, StoreView, ExchangeView, ReferralsView, \
    ProfileEdit, DepositView, WithdrawView

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),

    url(r'^$', auth(UserProfileView.as_view()),
        name='user-profile'),

    url(r'^profile_edit/$', auth(ProfileEdit.as_view(success_url = reverse_lazy('user-profile'))),
        name='user-profile-edit'),


    url(r'^collect/$', auth(CollectCoinsView.as_view(success_url = reverse_lazy('collect-coins'))),
        name='collect-coins'),

    url(r'^sell/$', auth(SellCoinsView.as_view(success_url = reverse_lazy('sell-coins'))),
        name='sell-coins'),

    url(r'^store/$', auth(StoreView.as_view(success_url = reverse_lazy('store'))),
        name='store'),

    url(r'^deposit/$', auth(DepositView.as_view()),
        name='deposit'),

    url(r'^exchange/$', auth(ExchangeView.as_view(success_url = reverse_lazy('exchange'))),
        name='exchange'),

    url(r'^withdraw/$', auth(WithdrawView.as_view(success_url = reverse_lazy('withdraw'))),
        name='withdraw'),

    url(r'^referrals/$', auth(ReferralsView.as_view()),
        name='referrals'),
)