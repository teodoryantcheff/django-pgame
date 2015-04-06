# coding=utf-8

from django.contrib.auth.models import Group

from custom_user.models import EmailUser
from solo.admin import SingletonModelAdmin
import account.models

from pgameapp.admin.actor import ActorAdmin
from pgameapp.admin.user import UserWithProfileAdmin
from pgameapp.admin.admin import GroupAdminWithCount, BlockProcessingHistoryAdmin, CryptoTransactionAdmin, \
    ReferralBonusPaymentAdmin, UserLedgerAdmin, WithdrawalRequestAdmin

from pgameapp.models import GameConfiguration, Actor, ManualGameStats, CryptoTransaction, \
    BlockProcessingHistory, ReferralBonusPayment, UserLedger, WithdrawalRequest

from django.contrib import admin

__author__ = 'Jailbreaker'


admin.site.site_header = 'MEGASITE Madafaka'
admin.site.site_title = 'MegaSite'

admin.site.unregister(Group)
admin.site.register(Group, GroupAdminWithCount)

admin.site.unregister(EmailUser)
admin.site.register(EmailUser, UserWithProfileAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)

admin.site.unregister(account.models.AccountDeletion)
admin.site.unregister(account.models.Account)
admin.site.unregister(account.models.SignupCode)
admin.site.unregister(account.models.EmailAddress)

admin.site.register(Actor, ActorAdmin)
admin.site.register(GameConfiguration, SingletonModelAdmin)
admin.site.register(ManualGameStats, SingletonModelAdmin)

admin.site.register(ReferralBonusPayment, ReferralBonusPaymentAdmin)

admin.site.register(CryptoTransaction, CryptoTransactionAdmin)
admin.site.register(BlockProcessingHistory, BlockProcessingHistoryAdmin)

admin.site.register(UserLedger, UserLedgerAdmin)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
