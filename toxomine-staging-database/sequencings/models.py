# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm

#####################################################################################################
#  Submission Properties
#  ---------------------
#  Sequencing
#####################################################################################################
"""
Class to hold Sequencing information
"""
class Sequencing(models.Model):
    name = models.CharField(max_length=100, null=False)
    platform = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_platform")
    instrument = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_instrument")
    version = models.CharField(max_length=10)
    read_length = models.IntegerField()
    read_type = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_read_type")

    class Meta:
        unique_together = ('name', 'platform', 'instrument', 'version', 'read_length', 'read_type')

    def __unicode__(self):
        return u"""{name}:{platform}:{instrument}:{version}""".format(
            name=self.name,
            platform=self.platform,
            instrument=self.instrument,
            version=self.version,
        )