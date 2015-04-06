from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.html import escape

__author__ = 'Jailbreaker'


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


class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_link', 'status', 'amount', 'to_address')  # , 'user__profile__balance_i')
    # list_display_links = ('user', )
    list_editable = ('status',)
    # fields = ('user', 'amount', 'to_address', 'status')
    readonly_fields = ('user', 'decided_by')
    list_filter = ('status', 'timestamp')
    # filter_horizontal = ('status',)
    list_select_related = ('user', )

    # noinspection PyMethodMayBeStatic
    def user_link(self, wreq):
        content_type = ContentType.objects.get_for_model(wreq.user.__class__)
        print 'app_label: {}, model: {}'.format(content_type.app_label, content_type.model)
        rev = reverse('admin:{app}_{model}_change'.format(app=content_type.app_label, model=content_type.model),
                      args=(wreq.user.id,))
        return '<a href="{link}">{label}</a>'.format(link=rev, label=escape(wreq.user))
    user_link.allow_tags = True
    user_link.short_description = "User"


class GroupAdminWithCount(GroupAdmin):
    # noinspection PyMethodMayBeStatic
    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'users'

    list_display = GroupAdmin.list_display + ('user_count',)
