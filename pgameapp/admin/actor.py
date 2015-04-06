# coding=utf-8
from django.contrib import admin
from django.db.models import Sum

__author__ = 'Jailbreaker'


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'output', 'is_active', 'num_as_bonus',  'image_tag', 'num_owned', 'total_output')
    list_filter = ('is_active', )
    ordering = ('price', )
    readonly_fields = ('image_tag',)
    # filter_horizontal = ('is_active', )

    # TODO list_select_related = ('useractorpwnership_set__num_actors', )

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


