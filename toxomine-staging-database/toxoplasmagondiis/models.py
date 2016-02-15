# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm
from organisms.models import Organism
from genes.models import Gene

#####################################################################################################
#  Submission Properties
#  ---------------------
#  ToxoplasmaMutant
#####################################################################################################

"""
 Class to hold ToxoplasmaMutant information
"""
class ToxoplasmaMutant(models.Model):
    name = models.CharField(max_length=255, null=False)
    target_name = models.CharField(max_length=255, blank=True)
    background = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_background")
    selection = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_selection")
    mutation_type = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_mutation_type")
    promoter = models.ForeignKey(OntologyTerm, null=True, related_name="%(app_label)s_%(class)s_promoter")
    #Relationships
    organism = models.ForeignKey(Organism, null=False, related_name="%(app_label)s_%(class)s_organism")
    target_gene = models.ForeignKey(Gene, null=True, related_name="%(app_label)s_%(class)s_target_gene")

    class Meta:
        unique_together = ('name', 'target_name', 'background', 'selection', 'mutation_type', 'organism')

    def __unicode__(self):
        return u"""{name}:{organism}""".format(
            name=self.name,
            organism=self.organism,
        )