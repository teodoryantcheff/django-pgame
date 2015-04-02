__author__ = 'Jailbreaker'

from django.conf import settings

CRYPTO_WALLET_CONNSTRING = '{proto}://{user}:{password}@{address}:{port}'.format(
    proto=settings.CRYPTO_WALLET_PROTO,
    user=settings.CRYPTO_WALLET_USER,
    password=settings.CRYPTO_WALLET_PASSWORD,
    address=settings.CRYPTO_WALLET_IP,
    port=settings.CRYPTO_WALLET_PORT
)

CRYPTO_WALLET_ADDRESS = '{proto}://{address}:{port}'.format(
    proto=settings.CRYPTO_WALLET_PROTO,
    address=settings.CRYPTO_WALLET_IP,
    port=settings.CRYPTO_WALLET_PORT
)