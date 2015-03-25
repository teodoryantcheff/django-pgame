from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import IntegrityError

from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from pgameapp.models import GameConfiguration, Actor, ActorProcurementHistory, CoinConversionHistory, UserProfile
from pgameapp.models import UserActorOwnership

__author__ = 'Jailbreaker'

User = get_user_model()  # TODO fixme


def buy_actor(request, actor):
    if not actor:
        raise ValidationError('Invalid Actor')

    user = request.user
    now = timezone.now()

    if actor.price > user.profile.balance_i:
        raise ValidationError('Insufficient funds')

    game_config = GameConfiguration.objects.get()

    last_coll = user.profile.last_coin_collection_time
    seconds = int((now - last_coll).total_seconds())

    # If user has actors and hasn;t collected
    if seconds > game_config.coin_collect_time*60 and user.profile.get_total_actors() > 0:
        raise ValidationError('Go collect your shit first')

    ua, created = UserActorOwnership.objects.get_or_create(
        user=user,
        actor=actor,
        defaults={'num_actors': 1}
    )

    if not created:
        ua.num_actors += 1

    ua.save()

    user.profile.balance_i -= actor.price
    user.profile.last_coin_collection_time = now
    user.profile.save()

    ActorProcurementHistory.objects.create(
        user=user,
        timestamp=now,
        actor=actor,
        price=actor.price
    )


def collect_coins(request):
    user = request.user
    game_config = GameConfiguration.objects.get()

    last_coll = user.profile.last_coin_collection_time
    now = timezone.now()

    seconds = int((now - last_coll).total_seconds())

    if seconds < game_config.coin_collect_time*60:
        raise ValidationError('Too soon')

    # TODO move this and the one in the view to a proper place
    # actors = user.actors.select_related('user', 'actor')
    actors = user.useractorownership_set.select_related('actor')
    sum_coins_generated = 0
    for actor in actors:
        sum_coins_generated += actor.num_actors * actor.actor.output * int(seconds/60)

    print('total collected {}'.format(sum_coins_generated))

    user.profile.balance_coins += sum_coins_generated
    user.profile.last_coin_collection_time = now
    user.profile.save()


def exchange__gc_w_to_i(request, gc_to_exchange):
    user = request.user
    game_config = GameConfiguration.objects.get()

    if gc_to_exchange > user.profile.balance_w:
        raise ValidationError('Not enough withdrdawal balance')

    bonus = (100 + game_config.w_to_i_conversion_bonus_percent) / 100.0

    user.profile.balance_w -= gc_to_exchange
    user.profile.balance_i += gc_to_exchange * bonus
    user.profile.save()

    # History.objects.create(
    #     user=user,
    #     timestamp=now,
    #     actor=a,
    #     price=a.price
    # ).save()


def sell_coins_to_gc(request, coins):
    user = request.user
    game_config = GameConfiguration.objects.get()

    if coins < game_config.min_coins_to_sell:
        raise ValidationError('Need to sell at least {}'.format(game_config.min_coins_to_sell))

    if coins > user.profile.balance_coins:
        raise ValidationError('Not enough coins in balance')

    game_currency = coins / game_config.coin_to_gc_rate

    investment_gc = game_currency * game_config.investment_balance_percent_on_sale / 100.0
    withdrawal_gc = game_currency - investment_gc

    user.profile.balance_i += investment_gc
    user.profile.balance_w += withdrawal_gc

    user.profile.balance_coins -= coins
    user.profile.save()

    now = timezone.now()
    CoinConversionHistory.objects.create(
        user=user,
        timestamp=now,
        coins=coins,
        game_currency=game_currency
    )


# This gets called after account signup
def create_userprofile(user_email, ref_info={}):

    user = User.objects.get(email=user_email)

    ref_code = ref_info.get('ref_code', '')
    ref_src = ref_info.get('ref_src', '')
    ref_cmp = ref_info.get('ref_cmp', '')

    # TODO ref source and ref campaign storage and usage

    try:
        referrer_user = User.objects.get(profile__referral_id=ref_code)
    except ObjectDoesNotExist:
        referrer_user = None


