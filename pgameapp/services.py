# coding=utf-8
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum

from django.utils import timezone
from django.core.exceptions import ValidationError

from pgameapp.models import GameConfiguration, ReferralBonusPayment, User
from pgameapp.models import UserActorOwnership
from pgameapp.models import UserLedger

__author__ = 'Jailbreaker'


def buy_actor(user, actor):
    if not actor:
        raise ValidationError('Invalid Actor')

    if actor.price > user.profile.balance_i:
        raise ValidationError('Insufficient funds')

    game_config = GameConfiguration.objects.get(pk=1)

    now = timezone.now()
    seconds = (now - user.profile.last_coin_collection_time).total_seconds()

    # If user has actors and hasn't collected
    if seconds > game_config.coin_collect_time*60 and user.get_total_actors() > 0:
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

    UserLedger.objects.log(user, UserLedger.BUY_ACTOR, -actor.price, data={'name': actor.name})


def collect_coins(user):
    game_config = GameConfiguration.objects.get(pk=1)

    last_coll = user.profile.last_coin_collection_time
    now = timezone.now()

    seconds = int((now - last_coll).total_seconds())

    if seconds < game_config.coin_collect_time*60:
        raise ValidationError('Too soon')

    uas, total = user.get_coins_generated(until=now)

    print('total collected {}'.format(total))

    user.profile.balance_coins += total
    user.profile.last_coin_collection_time = now
    user.profile.save()


def exchange__w2i(user, gc_to_exchange):
    game_config = GameConfiguration.objects.get(pk=1)

    if gc_to_exchange > user.profile.balance_w:
        raise ValidationError('Not enough withdrdawal balance')

    gc_to_exchange = Decimal(gc_to_exchange)
    bonus_percent = Decimal(100 + game_config.w_to_i_conversion_bonus_percent) / Decimal(100.0)
    to_receive = gc_to_exchange * bonus_percent

    user.profile.balance_w -= gc_to_exchange
    user.profile.balance_i += to_receive
    user.profile.save()

    UserLedger.objects.log(user, UserLedger.W2I_EXCHANGE, to_receive, data={'gc_exchanged': gc_to_exchange})


def sell_coins_to_gc(user, coins):
    game_config = GameConfiguration.objects.get(pk=1)

    if coins < game_config.min_coins_to_sell:
        raise ValidationError('Need to sell at least {}'.format(game_config.min_coins_to_sell))

    if coins > user.profile.balance_coins:
        raise ValidationError('Not enough coins in balance')

    game_currency = coins / game_config.coin_to_gc_rate

    investment_gc = game_currency * game_config.investment_balance_percent_on_sale / 100
    withdrawal_gc = game_currency - investment_gc

    user.profile.balance_i += investment_gc
    user.profile.balance_w += withdrawal_gc

    user.profile.balance_coins -= coins
    user.profile.save()

    UserLedger.objects.log(user, UserLedger.SELL_COINS, investment_gc,
                           data={'coins': coins, 'withdrawal_gc': withdrawal_gc})


def apply_payment(address, amount, transaction):
    """

    :param address:
    :param amount:
    :return:
    """

    game_config = GameConfiguration.objects.get(pk=1)

    try:
        # TODO real crypto to GC conversion rate needs to be added here too
        # amount = amount

        user = User.objects.\
            select_related('profile__referrer__profile').\
            get(profile__crypto_address=address)

        user.credit(amount)
        UserLedger.objects.log(user, UserLedger.PAYMENT, amount, transaction)

        if user.get_deposits_info() < 1:
            bonus = amount * Decimal(game_config.first_deposit_bonus_percent) / 100

            user.credit(bonus)
            UserLedger.objects.log(user, UserLedger.BONUS_FIRST_PAYMENT, bonus, transaction)

            print 'Added first deposit bonus of {:.2}'.format(bonus)

        user.profile.save()

        if user.profile.referrer:
            referrer = user.profile.referrer
            referrer.__class__ = User  # "cast" to proxy User model

            referral_bonus = amount * Decimal(game_config.affiliate_deposit_percent) / 100

            referrer.credit(referral_bonus)  #, UserLedger.BONUS_REFERRAL_PAYMENT, transaction)
            UserLedger.objects.log(referrer, UserLedger.BONUS_REFERRAL_PAYMENT, referral_bonus, transaction)

            ReferralBonusPayment.objects.create(
                user=referrer,
                referred_user=user,
                ref_source=user.profile.ref_source,
                ref_campaign=user.profile.ref_campaign,
                amount=referral_bonus
            )

            referrer.save()
            print 'Added referral bonus of {:.2} to to user {}'.format(referral_bonus, referrer)

        print 'Credited Ð {:.2} to {}'.format(amount, user)

    except User.DoesNotExist:
        print 'Owner of "{}" not found. Will credit to catchall address !'. format(address)  # TODO


def get_game_stats():
    now = timezone.now()
    return (
        # Total users
        User.objects.count(),
        # query_users_new_last_24h
        User.objects.filter(date_joined__gt=(now - timedelta(hours=24))).count(),
        # query_cash_reserve
        User.objects.all().aggregate(Sum('profile__balance_i')).values()[0] + \
        User.objects.all().aggregate(Sum('profile__balance_w')).values()[0]
    )