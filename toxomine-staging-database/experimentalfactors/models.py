# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm

#####################################################################################################
#  Submission Properties
#  ---------------------
#  ExperimentalFactor
#####################################################################################################
"""
Class to hold Experimental Factor information
"""
class ExperimentalFactor(models.Model):
    #Basic information
    name = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_name")
    value = models.CharField(max_length=100, blank=False)

    class Meta:
        unique_together = ('name', 'value',)

    def __unicode__(self):
        return u"""{name}:{value}""".format(
            name=self.name,
            value=self.value,
        )