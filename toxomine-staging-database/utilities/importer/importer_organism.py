# Python imports

# Core Django imports
from django.core.exceptions import ObjectDoesNotExist

# Local app imports
from organisms.models import Organism

######################################################################################################
##  Get Organism
######################################################################################################
def get_organism(taxon_id):
    try:
        organism = Organism.objects.get(taxon_id=taxon_id) # Load existing Organism from database
    except Organism.DoesNotExist:
        sys.exit('Organism does not exist')
    return organism