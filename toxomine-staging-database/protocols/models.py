# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm

#####################################################################################################
#  Protocol
#####################################################################################################
"""
 Custom manager for Protocol.
"""
class ProtocolManager(models.Manager):
    # Return the most current version of all protocols
    def get_queryset(self):
        return super(ProtocolManager, self).get_queryset().filter(current=True)

"""
 Class to hold Protocol information
"""
class Protocol(models.Model):
    name = models.CharField(max_length=255, null=False)
    current = models.BooleanField(default=True) # most current version of protocol
    version = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    protocol_type = models.ForeignKey(OntologyTerm, null=True, blank=True, related_name="%(app_label)s_%(class)s_protocol_type")    
    #Relationships
    previous_protocol = models.ForeignKey("Protocol", null=True, blank=True, related_name="%(app_label)s_%(class)s_previous_protocol")

    # Managers
    objects = models.Manager() # The default manager.
    protocol_objects = ProtocolManager() # The Protocol-specific manager.

    class Meta:
        unique_together = ('name', 'description', 'protocol_type')

    def __unicode__(self):
        return u"""{name}-v{version}""".format(
            name=self.name,
            version=self.version,
        )