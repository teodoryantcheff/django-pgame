from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext as _

from custom_user.admin import EmailUserAdmin
from custom_user.models import EmailUser
from solo.admin import SingletonModelAdmin

import account.models

from pgameapp.models import GameConfiguration, UserProfile, Actor, ManualGameStats, CryptoTransaction


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'output', 'is_active', 'num_as_bonus',  'image_tag')
    list_filter = ('is_active', )
    ordering = ('price', )
    readonly_fields = ('image_tag',)
    # filter_horizontal = ('is_active', )

#
# class UserInline(admin.StackedInline):
#     model = EmailUser
#     fk_name = 'userprofile'
#     can_delete = False
#     verbose_name_plural = 'user__FK'


# class UserProfileAdmin(admin.ModelAdmin):
#     # TODO http://stackoverflow.com/questions/14130174/django-foreign-key-value-in-a-list-display-admin
#     inlines = (UserInline, )
#
#     list_display = ('user', 'balance_i', 'balance_w', 'balance_coins')
#     # list_filter = ('is_staff', 'is_superuser', 'is_active', )#'groups')
#     # search_fields = ('user', )  # 'first_name', 'last_name')
#     # ordering = ('user', 'balance_i', 'balance_w', )
#     # filter_horizontal = ('groups', 'user_permissions',)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'profile'
    readonly_fields = ('signup_ip',)


class UserWithProfileAdmin(EmailUserAdmin):
    inlines = (UserProfileInline, )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser'),
#                                'groups', 'user_permissions')}),
                            'classes': ('collapse',)}),
        (_('Important dates'), {'fields':  ('last_login', 'date_joined'),
                                'classes': ('collapse',)}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )

    list_display = ('email', 'is_staff', 'date_joined', 'last_login', 'balance_i', 'balance_w', 'balance_coins')#, 'profile__balance_i', 'profile__balance_w', 'profile__balance_coins')
    # list_editable = ('is_staff',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')#'groups')
    search_fields = ('email', 'date_joined')
    ordering = ('-date_joined',)
    # filter_horizontal = ('groups', 'user_permissions',)

    def balance_i(self, obj):
        return obj.profile.balance_i
    balance_i.short_description = 'Investment'

    def balance_w(self, obj):
        return obj.profile.balance_w
    balance_w.short_description = 'Withdrawal'

    def balance_coins(self, obj):
        return obj.profile.balance_coins
    balance_coins.short_description = 'Coins'


class CryptoTransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'tx_type', 'user', 'crypto_currency', 'game_currency')
    list_filter = ('tx_type', )
    ordering = ('-timestamp', )
    # readonly_fields = ('image_tag',)

admin.site.site_header = 'MEGASITE Madafaka'
admin.site.site_title = 'MegaSite'

admin.site.unregister(Group)

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

admin.site.register(CryptoTransaction, CryptoTransactionAdmin)

