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