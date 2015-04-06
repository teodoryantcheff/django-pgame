from decimal import Decimal
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, UpdateView
from pgameapp.forms import WithdrawalForm, CollectCoinsForm, SellCoinsForm, StoreForm, ExchangeForm

from pgameapp.models import Actor, UserProfile, CryptoTransaction, UserLedger, WithdrawalRequest
from pgameapp.models.gameconfiguration import GameConfiguration
from pgameapp import  services


class CollectCoinsView(FormView):
    template_name = 'pgameapp/collectcoins.html'
    form_class = CollectCoinsForm
    # success_url = reverse_lazy('user-profile')

    def get_context_data(self, **kwargs):
        context = super(CollectCoinsView, self).get_context_data(**kwargs)
        user = self.request.user

        now = timezone.now()
        # uacg = user actors coins generated
        uacg, total = user.get_coins_generated(until=now)
        context['user_actors_generated'] = uacg
        context['total_generated'] = total

        # TODO remove, debug only
        context['seconds_since_last_collection'] = (now - user.profile.last_coin_collection_time).total_seconds()

        context['last_collection_datetime'] = user.profile.last_coin_collection_time
        context['now'] = now

        return context

    def get_form_kwargs(self):
        kwargs = super(CollectCoinsView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SellCoinsView(FormView):
    template_name = 'pgameapp/sell_coins.html'
    form_class = SellCoinsForm
    # success_url = reverse_lazy('user-profile')

    def get_form_kwargs(self):
        kwargs = super(SellCoinsView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        return {
            'coins_to_sell': self.request.user.profile.balance_coins,
        }

    def get_context_data(self, **kwargs):
        context = super(SellCoinsView, self).get_context_data(**kwargs)

        game_config = GameConfiguration.objects.get(pk=1)

        context['coin_to_gc_rate'] = game_config.coin_to_gc_rate
        context['game_currency'] = game_config.game_currency
        context['coin_collect_time'] = game_config.coin_collect_time
        context['coin_conversion_history'] = self.request.user.get_coin_conversion_history()
        return context


class UserProfileView(DetailView):
    template_name = 'pgameapp/userprofile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile


class StoreView(FormView):
    template_name = 'pgameapp/store.html'
    form_class = StoreForm
    # success_url = reverse_lazy('store')

    def get_form_kwargs(self):
        kwargs = super(StoreView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StoreView, self).get_context_data(**kwargs)

        user = self.request.user
        context['sellable_actors'] = Actor.sellable.all()
        context['owned_actors'] = user.get_owned_actors()
        context['actor_procurement_history'] = user.get_actor_procurement_history()

        return context


class ExchangeView(FormView):
    template_name = 'pgameapp/exchange.html'
    form_class = ExchangeForm
    # success_url = reverse_lazy('user-profile')

    def get_form_kwargs(self):
        kwargs = super(ExchangeView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        return {
            'gc_to_exchange': self.request.user.profile.balance_w,
        }

    def get_context_data(self, **kwargs):
        context = super(ExchangeView, self).get_context_data(**kwargs)

        game_config = GameConfiguration.objects.get(pk=1)

        context['game_currency'] = game_config.game_currency
        context['w_to_i_conversion_bonus_percent'] = game_config.w_to_i_conversion_bonus_percent

        bonus_percent = Decimal(100 + game_config.w_to_i_conversion_bonus_percent) / Decimal(100.0)
        context['would_receive'] = self.request.user.profile.balance_w * bonus_percent

        context['w2i_exchange_history'] = self.request.user.get_w2i_exchange_history()

        return context


class ReferralsView(ListView):
    template_name = 'pgameapp/referrals.html'
    context_object_name = 'user_referred_accounts'

    def get_queryset(self):
        return self.request.user.get_referrals()

    def get_context_data(self, **kwargs):
        context = super(ReferralsView, self).get_context_data(**kwargs)

        # context['referral_payment_stats'] = self.request.user.get_referral_payment_stats()
        context['referral_stats'] = self.request.user.get_referral_stats()
        # context['referral_signup_stats'] = self.request.user.get_referral_signup_stats()

        return context


class RefillView(ListView):
    template_name = 'pgameapp/refill.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return CryptoTransaction.objects.all()  #filter(user=self.request.user)
        # return self.request.user.select_related('referrals').order_by('-user__date_joined')


class WithdrawView(FormView):
    template_name = 'pgameapp/withdraw_request.html'
    form_class = WithdrawalForm
    # success_url = reverse_lazy('user-profile')

    def get_form_kwargs(self):
        kwargs = super(WithdrawView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        user = self.request.user
        # noinspection PyUnusedLocal
        to_address = ''

        try:
            last_withdrawal = WithdrawalRequest.objects.\
                filter(user=user, status=WithdrawalRequest.PAID).\
                order_by('-timestamp')[0]
            to_address = last_withdrawal.to_address
        except IndexError:
            to_address = 'enter a new address'

        return {
            'gc_to_withdraw': self.request.user.profile.balance_w,
            'to_address': to_address
        }

    def form_valid(self, form):
        user = self.request.user
        to_address = form.cleaned_data.get('to_address')
        gc_to_withdraw = form.cleaned_data.get('gc_to_withdraw')

        services.request_withdrawal(user, gc_to_withdraw, to_address)

        return super(WithdrawView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(WithdrawView, self).get_context_data(**kwargs)

        user = self.request.user

        game_config = GameConfiguration.objects.get(pk=1)
        context['game_config'] = game_config

        count_deposits, sum_deposits = user.get_deposits_info()
        context['count_deposits'] = count_deposits
        context['sum_deposits'] = sum_deposits

        context['withdrawal_request_history'] = user.get_withdrawal_request_history()

        context['game_currency'] = game_config.game_currency

        return context


class ProfileEdit(UpdateView):
    # form_class = ProfileEditForm
    # model = UserProfile
    fields = ['nickname']
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)