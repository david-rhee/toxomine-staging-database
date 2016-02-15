# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from general.models import Dbxref
from ontologies.models import OntologyTerm

#####################################################################################################
#  Based on Chado's organism module
#####################################################################################################
"""
 Class to hold organism information
"""
class Organism(models.Model):
    taxon_id = models.IntegerField(blank=False, unique=True)
    abbreviation = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True)
    common_name = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    # Relationship
    dbxrefs = models.ManyToManyField(Dbxref, blank=True, related_name="%(app_label)s_%(class)s_dbxrefs")
    organism_properties = models.ManyToManyField("OrganismProperty", blank=True, related_name="%(app_label)s_%(class)s_organism_properties")

    def __unicode__(self):
        return u"""{common_name}""".format(common_name=self.common_name)

"""
 Class to hold organism property information
""" 
class OrganismProperty(models.Model):
    organism = models.ForeignKey(Organism, null=False, related_name="%(app_label)s_%(class)s_organism" )
    organism_property_type = models.ForeignKey(OntologyTerm, on_delete=models.CASCADE, null=False, blank=False, related_name="%(app_label)s_%(class)s_organism_property_type")
    organism_property_value = models.ForeignKey(OntologyTerm, on_delete=models.CASCADE, null=True, blank=True, related_name="%(app_label)s_%(class)s_organism_property_value")
    value = models.TextField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('organism', 'organism_property_type', 'organism_property_value', 'value')

    def __unicode__(self):
        return u"""{organism_property_type}:{organism_property_value}:{value}""".format(
            organism_property_type=self.organism_property_type,
            organism_property_value=self.organism_property_value,
            value=self.value,
        )