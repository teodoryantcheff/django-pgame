# _TODO https://github.com/jcugat/django-custom-user
# TODO https://github.com/dyve/django-bootstrap3
# _TODO signups
# _TODO login ip
# _TODO select_related vs prefetch_related
# TODO Referrals management and reports
# _TODO dogecoin interfaces
# TODO test transactions management
# _TODO bonuses
# TODO in site games
# TODO tests
# TODO user action history
# ^ https://django-simple-history.readthedocs.org/en/latest/

# _TODO Profile, after login
# _TODO Shop - buy actors
# _TODO Sklad - convert coins to silver
# _TODO Sell to GC
# _TODO Exchange - withdrawal GC to investment GC
# _TODO referrer stats
# _TODO Top up balance (doge transfer confirmation)
# TODO Request payout / withdrawal
# TODO Profile settings
# _TODO game stats box


# TODO https://github.com/tomatohater/django-unfriendly
# TODO https://docs.djangoproject.com/en/1.7/ref/contrib/admin/actions/
# TODO http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/
# TODO https://github.com/pydanny/cookiecutter-django/

# TODO Proper ValidatoinError - https://docs.djangoproject.com/en/1.7/ref/forms/validation/#raising-validationerror

#  Separation of business logic and data access in django
# TODO http://stackoverflow.com/questions/12578908/separation-of-business-logic-and-data-access-in-django
# TODO http://mauveweb.co.uk/posts/2014/08/organising-django-projects.html

from django.db.backends.signals import connection_created


def activate_foreign_keys(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('PRAGMA journal_mode = MEMORY;')
        cursor.execute('PRAGMA main.temp_store = MEMORY;')
        cursor.execute('PRAGMA cache_size = 8192;')  # in 1k pages
        # cursor.execute('PRAGMA cache_size = n_of_pages;')

connection_created.connect(activate_foreign_keys)