# Python imports

# Core Django imports
from django.core.exceptions import ValidationError

# Local app imports
from microarrays.models import MicroArray

######################################################################################################
##  Get or Create MicroArray
######################################################################################################
def get_microarray(name, platform, microarray_format, version, genome_name, genome_version):
    #check if microarray, if so return, if not create new
    try:
        microarray = MicroArray(name=name, platform=platform, microarray_format=microarray_format, version=version, genome_name=genome_name, genome_version=genome_version)
        microarray.validate_unique()
        microarray.save()

    except ValidationError as e:
        microarray = MicroArray.objects.get(name=name, platform=platform, microarray_format=microarray_format, genome_name=genome_name, genome_version=genome_version)
    
    return microarray
