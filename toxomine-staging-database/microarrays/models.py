# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm

#####################################################################################################
#  Submission Properties
#  ---------------------
#  MicroArray
#####################################################################################################
"""
Class to hold Data Attribute information
"""
class MicroArray(models.Model):
    name = models.CharField(max_length=100, null=False)
    platform = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_platform")
    microarray_format = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_microarray_format")
    version = models.CharField(max_length=10, blank=True)
    genome_name = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_genome_name")
    genome_version = models.CharField(max_length=10)

    class Meta:
        unique_together = ('name', 'platform', 'microarray_format', 'genome_name', 'genome_version',)

    def __unicode__(self):
        return u"""{name}:{platform}""".format(
            name=self.name,
            platform=self.platform,
        )