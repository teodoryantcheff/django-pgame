from django.contrib.auth import get_user_model
from django.db.models import Sum

from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, UpdateView

from pgameapp.forms import SellCoinsForm, CollectCoinsForm, StoreForm, ExchangeForm

from pgameapp.models import UserActorOwnership, Actor, ActorProcurementHistory, CoinConversionHistory, UserProfile, \
    CryptoTransaction, User
from pgameapp.models.gameconfiguration import GameConfiguration

# _TODO Profile, after login
# _TODO Shop - buy actors
# _TODO Sklad - convert coins to silver
# _TODO Sell to GC
# TODO GAMES
# _TODO Exchange - withdrawal GC to investment GC
# TODO referrer stats
# _TODO Top up balance (doge transfer confirmation)
# TODO Request payout / withdrawal
# TODO Profile settings
# _TODO game stats box


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

    def get_context_data(self, **kwargs):
        context = super(SellCoinsView, self).get_context_data(**kwargs)

        game_config = GameConfiguration.objects.get(pk=1)

        context['coin_to_gc_rate'] = game_config.coin_to_gc_rate
        context['game_currency'] = game_config.game_currency
        context['coin_collect_time'] = game_config.coin_collect_time
        context['coin_conversion_history'] = CoinConversionHistory.objects.filter(user=self.request.user)[:10]
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

    def get_context_data(self, **kwargs):
        context = super(ExchangeView, self).get_context_data(**kwargs)

        game_config = GameConfiguration.objects.get(pk=1)

        context['game_currency'] = game_config.game_currency
        context['w_to_i_conversion_bonus_percent'] = game_config.w_to_i_conversion_bonus_percent

        return context


class ReferralsView(ListView):
    template_name = 'pgameapp/referrals.html'
    context_object_name = 'user_referred_accounts'

    def get_queryset(self):
        return self.request.user.get_referrals()

    def get_context_data(self, **kwargs):
        context = super(ReferralsView, self).get_context_data(**kwargs)

        context['referral_payment_stats'] = self.request.user.get_referral_payment_stats()
        context['referral_signup_stats'] = self.request.user.get_referral_signup_stats()

        return context

class RefillView(ListView):
    template_name = 'pgameapp/refill.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return CryptoTransaction.objects.all()  #filter(user=self.request.user)
        # return self.request.user.select_related('referrals').order_by('-user__date_joined')


class ProfileEdit(UpdateView):
    # form_class = ProfileEditForm
    # model = UserProfile
    fields = ['nickname']
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)

# def get_name(request):
# # if this is a POST request we need to process the form data
# if request.method == 'POST':
# # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, 'name.html', {'form': form})

# class StoreView2(ListView):
#     template_name = 'pgameapp/store2.html'
#     context_object_name = 'sellable_actors'
#
#     def get_queryset(self):
#         return Actor.objects.filter(is_active=True, users=self.request.user)\
#             .annotate(sum_user_owned=Sum('useractorownership__num_actors'))
#
#     def get_context_data(self, **kwargs):
#         context = super(StoreView2, self).get_context_data(**kwargs)
#
#         context['actor_procurement_history'] = ActorProcurementHistory.objects\
#             .filter(user=self.request.user) \
#             .order_by('-timestamp') \
#             .select_related('actor')[:10]
#
#         return context
#
#
# class BuyFormView(FormView):
#     form_class = BuyForm
#
#     def form_valid(self, form):
#         print 'form_valid'
#         return super(BuyFormView, self).form_valid(form)
#
#     def form_invalid(self, form):
#         print 'form_invalid'
#         return super(BuyFormView, self).form_invalid(form)