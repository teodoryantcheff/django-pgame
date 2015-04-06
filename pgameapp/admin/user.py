from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from custom_user.admin import EmailUserAdmin

from pgameapp.models import UserProfile, UserActorOwnership


__author__ = 'Jailbreaker'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'profile'
    readonly_fields = ('signup_ip', 'referrer')
    max_num = 1
    extra = 0


class GroupListFilter(SimpleListFilter):
    title = 'group'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        groups = Group.objects.all()
        items = ()
        for group in groups:
            items += ((unicode(group.id), unicode(group.name),),)
        return items

    def queryset(self, request, queryset):
        group_id = request.GET.get(self.parameter_name, None)
        if group_id:
            return queryset.filter(groups=group_id)
        return queryset


class UserActorOwnershipInline(admin.TabularInline):
    model = UserActorOwnership
    extra = 0
    fields = ('actor', 'image', 'num_actors')
    readonly_fields = ('actor', 'image')
    verbose_name_plural = 'Actors'
    can_delete = False

    # noinspection PyMethodMayBeStatic
    def image(self, ua):
        print ua.actor.image_tag()
        return mark_safe(ua.actor.image_tag())
    image.short_description = 'Image'
    image.allow_tags = True

    def has_add_permission(self, request):
        return False


class UserWithProfileAdmin(EmailUserAdmin):
    inlines = (UserProfileInline, UserActorOwnershipInline)

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
        p = sorted([u'<span title="{}">{}</span>'.format(x, short_name(x)) for x in u.groups.all()])
        # p += ['+'] if u.user_permissions.count() else []  # permissions
        return mark_safe(u'<span style="white-space: nowrap">{}</span>'.format(', '. join(p)))
    roles.allow_tags = True
    roles.short_description = u'Grp'

    list_display = ('email', 'roles', 'is_active', 'balance_i', 'balance_w', 'balance_coins',
                    'date_joined', 'last_login')
    list_filter = ('is_active', 'date_joined', GroupListFilter, 'is_staff')
    search_fields = ('email', 'date_joined')  #, 'profile__singup_ip')

    ordering = ('-date_joined',)

    filter_horizontal = ('groups',)

    actions = ('mark_as_cheaters', )
    list_select_related = ('profile',)

    # noinspection PyMethodMayBeStatic
    def balance_i(self, obj):
        return '{:.3f}'.format(obj.profile.balance_i)
    balance_i.short_description = 'inv'
    balance_i.admin_order_field = 'profile__balance_i'

    # noinspection PyMethodMayBeStatic
    def balance_w(self, obj):
        return '{:.3f}'.format(obj.profile.balance_w)
    balance_w.short_description = 'wth'
    balance_w.admin_order_field = 'profile__balance_w'

    # noinspection PyMethodMayBeStatic
    def balance_coins(self, obj):
        return obj.profile.balance_coins
    balance_coins.short_description = 'coins'
    balance_coins.admin_order_field = 'profile__balance_coins'

    def mark_as_cheaters(self, request, queryset):
        g = Group.objects.get(name='cheaters')
        rows_updated = 0  # queryset.update(status='p')
        for u in queryset:
            u.groups.remove(g)
            rows_updated += 1

        if rows_updated == 1:
            message_bit = '1 user was'
        else:
            message_bit = '%s users were' % rows_updated
        self.message_user(request, "%s successfully marked as CHEATER." % message_bit)
    mark_as_cheaters.short_description = 'Mark fuckers as cheaters'

