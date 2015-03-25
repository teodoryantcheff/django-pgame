from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils.timezone import now


__author__ = 'Jailbreaker'


User = get_user_model()

query_users_total = User.objects.count()
query_users_new_last_24h = User.objects.filter(date_joined__gt=(now() - timedelta(hours=24))).count()
query_cash_reserve = User.objects.all().aggregate(Sum('profile__balance_i')).values()[0]\
                     + User.objects.all().aggregate(Sum('profile__balance_w')).values()[0]
