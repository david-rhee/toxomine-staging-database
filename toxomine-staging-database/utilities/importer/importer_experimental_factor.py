# Python imports

# Core Django imports
from django.core.exceptions import ValidationError

# Local app imports
from experimentalfactors.models import ExperimentalFactor

######################################################################################################
##  Get or Create Experimental Factor
######################################################################################################
def get_experimental_factor(name, value):
    #check if experimental_factor exists, if so return, if not create new
    try:
        experimental_factor = ExperimentalFactor(name=name, value=value)
        experimental_factor.validate_unique()
        experimental_factor.save()

    except ValidationError as e:
        experimental_factor = ExperimentalFactor.objects.get(name=name, value=value)
    
    return experimental_factor