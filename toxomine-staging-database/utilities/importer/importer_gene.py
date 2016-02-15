# Python imports

# Core Django imports
from django.core.exceptions import ObjectDoesNotExist

# Local app imports
from genes.models import Gene

######################################################################################################
##  Get Gene
######################################################################################################
def get_gene(gene_id):
    try:
        gene = Gene.objects.get(gene_id=gene_id) # Load existing Organism from database
    except Gene.DoesNotExist:
        sys.exit('Gene does not exist')
    return gene