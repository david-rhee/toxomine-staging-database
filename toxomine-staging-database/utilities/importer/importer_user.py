# Python imports
import json, urllib2

# Core Django imports
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Local app imports

######################################################################################################
##  Get User
######################################################################################################
def get_user(username):
    try:
        user = User.objects.get(username=username) # Load existing User from database
    except User.DoesNotExist:
        sys.exit('User does not exist')
    return user