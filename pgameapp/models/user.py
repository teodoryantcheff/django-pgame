from django.db import models
from django.db.models import Count, Sum
from custom_user.models import EmailUser
from pgameapp.models import WithdrawalRequest

from pgameapp.models.ledger import UserLedger


__author__ = 'Jailbreaker'


class AdminsManager(models.Manager):
    def get_queryset(self):
        return super(AdminsManager, self).get_queryset().filter(is_staff=True)


class User(EmailUser):
    class Meta:
        proxy = True

    objects = models.Manager()
    admins = AdminsManager()

    def credit(self, amount):
        """
        Credits user's "investment" balance

        :param amount:
        :param why: Why is the user getting credited. Types in UserLedger.
        :param transaction:
        :return: nothing
        """
        self.profile.balance_i += amount

    def debit(self, amount):
        """
        Debits user's .... TODO

        :param amount:
        :param why:
        :param transaction:
        :return:
        """
        pass

    def get_referral_stats(self):
        return self.referrals.values('ref_source', 'ref_campaign').distinct().\
            annotate(
                signups=Count('user'),
                amount_paid=Sum('user__ref_payments__amount'),
                count_payments=Count('user__ref_payments__user'),
            ).order_by()

    # def get_referral_payment_stats(self):
    #     # result = ReferralBonusPayment.objects.\
    #     #     values('referred_user__profile__ref_source', 'referred_user__profile__ref_campaign').\
    #     #     distinct().\
    #     #     annotate(count=Count('id'), sum=Sum('amount'), signups=Count('referred_user__profile'))
    #
    #     result = ReferralBonusPayment.objects.filter(user=self).\
    #         values('ref_source', 'ref_campaign').distinct().\
    #         annotate(count=Count('user'), sum=Sum('amount')).order_by('-sum')
    #     return result
    #
    # def get_referral_signup_stats(self):
    #     return self.referrals.\
    #         values('ref_source', 'ref_campaign').distinct().\
    #         annotate(signups=Count('user')).order_by('-signups')

    def get_referrals(self):
        return User.objects.filter(profile__referrer=self).order_by('-date_joined')

    def get_deposits_info(self):
        return tuple(UserLedger.objects.filter(user=self, type=UserLedger.PAYMENT).
                     aggregate(count=Count('id'), sum=Sum('amount')).
                     values())

    def get_total_actors(self):
        return self.useractorownership_set.aggregate(Sum('num_actors')).values()[0]

    def get_owned_actors(self):
        # return Actor.objects.filter(users=self).annotate(sum_user_owned=Sum('useractorownership__num_actors'))
        return self.useractorownership_set.select_related('actor').all()  #.annotate(sum_user_owned=Sum('useractorownership__num_actors'))

    def get_actor_procurement_history(self):
        # return ActorProcurementHistory.objects.filter(user=self).select_related('actor')[:10]
        return UserLedger.objects.filter(user=self, type=UserLedger.BUY_ACTOR)

    def get_coin_conversion_history(self):
        return UserLedger.objects.filter(user=self, type=UserLedger.SELL_COINS)

    def get_w2i_exchange_history(self):
        return UserLedger.objects.filter(user=self, type=UserLedger.W2I_EXCHANGE)


    def get_withdrawal_request_history(self):
        return WithdrawalRequest.objects.filter(user=self)  #.order_by('status')


    def get_coins_generated(self, until):
        uas = self.useractorownership_set.select_related('actor').all()
        last_collection_datetime = self.profile.last_coin_collection_time
        seconds = int((until - last_collection_datetime).total_seconds())

        # TODO math and account for min collect time
        generated = [int(ua.num_actors * ua.actor.output/3600 * seconds) for ua in uas]
        total = sum(generated)

        return zip(uas, generated), total

    def set_crypto_address(self, crypto_adderess):
        self.profile.crypto_address = crypto_adderess

    def set_referral_info(self, ref_code, ref_source='', ref_campaign=''):
        """
        Sets referral info. Does NOT save() after. Call save() yourself.

        :param ref_code: Referral code
        :param ref_source: Referral source
        :param ref_campaign: Referral campaign
        :return:
        """
        if ref_code:
            try:
                self.prfile.referrer = User.objects.get(profile__referral_id=ref_code)
                self.prfile.ref_source = ref_source
                self.prfile.ref_campaign = ref_campaign
            except User.DoesNotExist:
                print 'Account with referral_id {} does not exist. Ignoring'.format(ref_code)
