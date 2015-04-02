# coding=utf-8
from decimal import Decimal

from django.utils import timezone
from django.core.exceptions import ValidationError

from pgameapp.models import GameConfiguration, ActorProcurementHistory, CoinConversionHistory, ReferralStats, User
from pgameapp.models import UserActorOwnership
from pgameapp.models.history import UserLedger

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

    ActorProcurementHistory.objects.create(
        user=user,
        timestamp=now,
        actor=actor,
        price=actor.price
    )


def collect_coins(user):
    game_config = GameConfiguration.objects.get(pk=1)

    last_coll = user.profile.last_coin_collection_time
    now = timezone.now()

    seconds = int((now - last_coll).total_seconds())

    if seconds < game_config.coin_collect_time*60:
        raise ValidationError('Too soon')

    uas, total = user.get_coins_generated()

    print('total collected {}'.format(total))

    user.profile.balance_coins += total
    user.profile.last_coin_collection_time = now
    user.profile.save()


def exchange__gc_w_to_i(user, gc_to_exchange):
    game_config = GameConfiguration.objects.get(pk=1)

    if gc_to_exchange > user.profile.balance_w:
        raise ValidationError('Not enough withdrdawal balance')

    gc_to_exchange = Decimal(gc_to_exchange)
    bonus = Decimal(100 + game_config.w_to_i_conversion_bonus_percent) / Decimal(100.0)

    user.profile.balance_w -= gc_to_exchange
    user.profile.balance_i += gc_to_exchange * bonus
    user.profile.save()

    # History.objects.create(
    #     user=user,
    #     timestamp=now,
    #     actor=a,
    #     price=a.price
    # ).save()


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

    now = timezone.now()
    CoinConversionHistory.objects.create(
        user=user,
        timestamp=now,
        coins=coins,
        game_currency=game_currency
    )


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

        user.credit(amount, UserLedger.PAYMENT, transaction)

        num_deposits = user.get_num_deposits()

        if num_deposits < 1:
            bonus = amount * Decimal(game_config.first_deposit_bonus_percent) / 100
            user.credit(bonus, UserLedger.BONUS_FIRST_PAYMENT, transaction)
            print 'Added first deposit bonus of {:.2}'.format(bonus)

        user.profile.save()

        if user.profile.referrer:
            referrer = user.profile.referrer
            referrer.__class__ = User  # "cast" to proxy User model

            referral_bonus = amount * Decimal(game_config.affiliate_deposit_percent) / 100

            referrer.credit(referral_bonus, UserLedger.BONUS_REFERRAL_PAYMENT, transaction)

            ReferralStats.objects.create(
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