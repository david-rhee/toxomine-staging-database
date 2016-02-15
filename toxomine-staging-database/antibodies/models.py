# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from genes.models import Gene
from ontologies.models import OntologyTerm

#####################################################################################################
#  Submission Properties
#  ---------------------
#  Antibody
#####################################################################################################
"""
 Class to hold Antibody information
"""
class Antibody(models.Model):
    name = models.CharField(max_length=255, null=False) # Name of antibody i.e. anti-HA, anti-GCN5b
    target_name = models.CharField(max_length=255, blank=True) # Name of protein target i.e. GCN5b
    tagged = models.BooleanField(default=False) # If True, define tag name
    tag_target = models.CharField(max_length=255, blank=True) # HA
    source = models.CharField(max_length=255, blank=True)
    catalog_number = models.CharField(max_length=50, blank=True)
    epitope = models.CharField(max_length=255, blank=True)
    lot_number = models.CharField(max_length=255, blank=True)
    ifa_localization = models.CharField(max_length=255, blank=True)
    chip_peaks = models.CharField(max_length=255, blank=True)
    monoclonal = models.BooleanField(default=False)
    isotype = models.CharField(max_length=255, blank=True)
    immunogen_source = models.CharField(max_length=255, blank=True)
    conjugation = models.CharField(max_length=255, blank=True)
    validated = models.BooleanField(default=False)
    url = models.URLField(max_length=255, blank=True)
    #Ontologies
    animal_host = models.ForeignKey(OntologyTerm, null=True, related_name="%(app_label)s_%(class)s_animal_host")
    #Relationships
    target_gene = models.ForeignKey(Gene, null=True, related_name="%(app_label)s_%(class)s_taget_gene", verbose_name="Antibody's target gene")
    
    class Meta:
        unique_together = ('name', 'target_name', 'tagged')

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)