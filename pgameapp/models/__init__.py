# __init__.py
# noinspection PyUnresolvedReferences
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

from actors import UserActorOwnership, Actor
from userprofile import UserProfile
from gameconfiguration import GameConfiguration

from history import *
from models import *
