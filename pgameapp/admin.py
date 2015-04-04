# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from custom_user.admin import EmailUserAdmin
from custom_user.models import EmailUser
from solo.admin import SingletonModelAdmin
import account.models

from pgameapp.models import GameConfiguration, UserProfile, Actor, ManualGameStats, CryptoTransaction, \
    BlockProcessingHistory, ReferralBonusPayment, UserLedger


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'output', 'is_active', 'num_as_bonus',  'image_tag', 'num_owned', 'total_output')
    list_filter = ('is_active', )
    ordering = ('price', )
    readonly_fields = ('image_tag',)
    # filter_horizontal = ('is_active', )

    # noinspection PyMethodMayBeStatic
    def num_owned(self, a):
        return a.useractorownership_set.aggregate(Sum('num_actors')).values()[0]
    num_owned.short_description = u'№'

    def total_output(self, a):
        return self.num_owned(a) * a.output
    total_output.short_description = u'Σo/h (GC)'

    def get_actions(self, request):
        #Disable delete
        actions = super(ActorAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

    def has_add_permission(self, request):
        # Force the add button to be on
        return True


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'profile'
    readonly_fields = ('signup_ip', 'referrer')
    max_num = 1
    extra = 0


class UserWithProfileAdmin(EmailUserAdmin):
    inlines = (UserProfileInline, )

    fieldsets = (
        (None,                  {'fields': ('email', 'password')}),

        (_('Permissions'),      {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',),  # 'user_permissions'),
                                 'classes': ('collapse',)}),

        (_('Important dates'),  {'fields':  ('last_login', 'date_joined'),
                                 'classes': ('collapse',)}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )

    # noinspection PyMethodMayBeStatic
    def roles(self, u):
        #short_name = unicode # function to get group name
        short_name = lambda s: unicode(s)[:1].upper()  # first letter of a group
        p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in u.groups.all()])
        # p += ['+'] if u.user_permissions.count() else []
        value = ', '.join(p)
        return mark_safe("<nobr>%s</nobr>" % value)
    roles.allow_tags = True
    roles.short_description = u'G'

    list_display = ('email', 'roles', 'is_active', 'balance_i', 'balance_w', 'balance_coins',
                    'date_joined', 'last_login')
    # list_editable = ('is_staff',)
    list_filter = ('is_active', 'date_joined',)
    search_fields = ('email', 'date_joined')
    ordering = ('-date_joined',)
    # filter_horizontal = ('groups',) #, 'is_active', 'user_permissions',)

    # noinspection PyMethodMayBeStatic
    def balance_i(self, obj):
        return obj.profile.balance_i
    balance_i.short_description = 'inv'

    # noinspection PyMethodMayBeStatic
    def balance_w(self, obj):
        return obj.profile.balance_w
    balance_w.short_description = 'wth'

    # noinspection PyMethodMayBeStatic
    def balance_coins(self, obj):
        return obj.profile.balance_coins
    balance_coins.short_description = 'coins'


class CryptoTransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'tx_type', 'amount', 'address')
    list_filter = ('tx_type', 'timestamp')
    ordering = ('-timestamp', )
    # readonly_fields = ('user',)


class BlockProcessingHistoryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'blockhash', 'blockheight')
    readonly_fields = ('timestamp', 'blockhash', 'blockheight')
    ordering = ('-timestamp', )

    def get_actions(self, request):
        #Disable delete
        actions = super(BlockProcessingHistoryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False


class ReferralBonusPaymentAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'referred_user', 'amount', 'ref_source', 'ref_campaign')
    readonly_fields = ('timestamp', 'user', 'referred_user')
    exclude = ('ref_source', 'ref_campaign')


class UserLedgerAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'type', 'amount', 'data')
    list_filter = ('timestamp', 'type')


class GroupAdminWithCount(GroupAdmin):
    # noinspection PyMethodMayBeStatic
    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'users'

    list_display = GroupAdmin.list_display + ('user_count',)
########################################################################################################################

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
