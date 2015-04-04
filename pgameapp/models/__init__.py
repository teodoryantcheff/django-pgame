# __init__.py

from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

DECIMAL_DECIMAL_PLACES = 5
DECIMAL_MAX_DIGITS = DECIMAL_DECIMAL_PLACES + 11

from actors import UserActorOwnership, Actor
from userprofile import UserProfile
from gameconfiguration import GameConfiguration
from manualgamestats import ManualGameStats


from history import *
from user import User
from ledger import UserLedger
from models import *

from wallet import BlockProcessingHistory, CryptoTransaction
