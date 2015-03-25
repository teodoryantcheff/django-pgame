from pgameapp import queries
from pgameapp.models import UserProfile, ManualGameStats, GameConfiguration

__author__ = 'Jailbreaker'


def remote_ip(request):
    return {'remote_ip': request.META['REMOTE_ADDR']}


def user_profile(request):
    profile = {}
    if request.user.is_authenticated():
        profile = request.user.profile

    return {'userprofile_tp': profile}


def game_currency(request):
    return {'game_currency': GameConfiguration.objects.get(pk=1).game_currency}


def game_statistics(request):
    manual = ManualGameStats.objects.get(pk=1)
    gamestats = {
        'users_total': manual.users_total if manual.users_total > 0 else queries.query_users_total,
        'users_new_last_24h': manual.users_new_last_24 if manual.users_new_last_24 > 0 else queries.query_users_new_last_24h,
        'cash_reserve': manual.cash_reserve if manual.cash_reserve > 0 else queries.query_cash_reserve
    }
    return {'gamestats': gamestats}