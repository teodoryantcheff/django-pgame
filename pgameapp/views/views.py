from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

from django.utils import timezone
from django.views.generic import DetailView, TemplateView, FormView, ListView

from pgameapp.forms import SellCoinsForm, CollectCoinsForm, StoreForm, ExchangeForm

from pgameapp.models import UserActorOwnership, Actor, ActorProcurementHistory, CoinConversionHistory
from pgameapp.models.gameconfiguration import GameConfiguration

# _TODO Profile, after login
# _TODO Shop - buy actors
# _TODO Sklad - convert coins to silver
# _TODO Sell to GC
# TODO GAMES
# _TODO Exchange - withdrawal GC to investment GC
# TODO referrer stats
# TODO Top up balance (doge transfer confirmation)
# TODO Request payout / withdrawal
# TODO Profile settings
# TODO game stats box

User = get_user_model()  # TODO fixme


class CollectCoinsView(FormView):
    template_name = 'pgameapp/collectcoins.html'
    form_class = CollectCoinsForm
    # success_url = reverse_lazy('user-profile')

    def get_context_data(self, **kwargs):
        context = super(CollectCoinsView, self).get_context_data(**kwargs)
        user = self.request.user

        # qs = UserActorOwnership.objects\
        qs = user.useractorownership_set\
            .select_related('actor')\
            .order_by('actor__id')

        last_collection_datetime = user.profile.last_coin_collection_time
        now = timezone.now()
        seconds = int((now - last_collection_datetime).total_seconds())

        generated = [ua.num_actors * ua.actor.output * int(seconds / 60) for ua in qs]

        context['user_actors'] = zip(qs, generated)

        # print 'seconds since last collection', seconds
        context['seconds_since_last_collection'] = seconds

        context['last_collection_datetime'] = last_collection_datetime
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

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)

        context['user_referred_count'] = User.objects\
            .filter(profile__referrer=self.request.user)\
            .count()

        return context


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

        context['sellable_actors'] = Actor.objects\
            .filter(is_active=True, users=self.request.user)\
            .annotate(sum_user_owned=Sum('useractorownership__num_actors'))

        context['actor_procurement_history'] = ActorProcurementHistory.objects\
            .filter(user=self.request.user) \
            .order_by('-timestamp') \
            .select_related('actor')[:10]

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

        game_config = GameConfiguration.objects.get()

        context['game_currency'] = game_config.game_currency
        context['w_to_i_conversion_bonus_percent'] = game_config.w_to_i_conversion_bonus_percent

        return context


class ReferralsView(ListView):
    template_name = 'pgameapp/referrals.html'
    context_object_name = 'user_referred_accounts'

    def get_queryset(self):
        return User.objects\
            .filter(profile__referrer=self.request.user)\
            .order_by('-date_joined')


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