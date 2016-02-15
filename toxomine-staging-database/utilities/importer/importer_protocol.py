# Python imports

# Core Django imports
from django.core.exceptions import ValidationError

# Local app imports
from protocols.models import Protocol

######################################################################################################
##  Get or Create Protocol
######################################################################################################
def get_protocol(name, description, protocol_type):
    #check if protocol exists, if so return, if not create new
    try:
        protocol = Protocol(name=name, description=description, protocol_type=protocol_type)
        protocol.validate_unique()
        protocol.save()

    except ValidationError as e:
        protocol = Protocol.objects.get(name=name, description=description, protocol_type=protocol_type)
    
    return protocol