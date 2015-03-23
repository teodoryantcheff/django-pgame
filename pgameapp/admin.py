from custom_user.admin import EmailUserAdmin
from custom_user.models import EmailUser
from solo.admin import SingletonModelAdmin
from django.contrib import admin

from pgameapp.models import GameConfiguration, UserProfile, Actor, UserActorOwnership, ManualGameStats


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'output', 'is_active', 'image_tag')
    list_filter = ('is_active', )
    # search_fields = ('user', )  # 'first_name', 'last_name')
    ordering = ('name', )  # 'balance_i', 'balance_w', )
    readonly_fields = ('image_tag',)
    # filter_horizontal = ('is_active', )


class UserProfileAdmin(admin.ModelAdmin):
    # TODO http://stackoverflow.com/questions/14130174/django-foreign-key-value-in-a-list-display-admin
    # inlines = (UserActorOwnershipInLine, )

    list_display = ('user', 'balance_i', 'balance_w', 'balance_coins')
    # list_filter = ('is_staff', 'is_superuser', 'is_active', )#'groups')
    # search_fields = ('user', )  # 'first_name', 'last_name')
    # ordering = ('user', 'balance_i', 'balance_w', )
    # filter_horizontal = ('groups', 'user_permissions',)



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'

class UserwithProfileAdmin(EmailUserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('email', 'is_staff', 'profile')#'profile__balance_i', 'profile__balance_w', 'profile__balance_coins')

admin.site.unregister(EmailUser)
admin.site.register(EmailUser, UserwithProfileAdmin)


# class MyAdminSite(AdminSite):
#     site_header = 'MEGASITE Madafaka'
#     site_title = 'MegaSite'

admin.site.site_header = 'MEGASITE Madafaka'
admin.site.site_title = 'MegaSite'

admin.site.register(GameConfiguration, SingletonModelAdmin)
admin.site.register(ManualGameStats, SingletonModelAdmin)
#
# admin_site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
# # admin_site.register(UserActorOwnership, OwnershipAdmin)
# admin_site.register(Actor, ActorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(UserActorOwnership)

# TODO Groups and permissions
# admin_site.register(Group, GroupAdmin)
# admin_site.register(Question, QuestionAdmin)

