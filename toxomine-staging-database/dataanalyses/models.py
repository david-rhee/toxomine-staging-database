# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm

#####################################################################################################
#  Submission Properties
#  ---------------------
#  DataAnalysis
#####################################################################################################
"""
 Class to hold Data Analysis information
"""
class DataAnalysis(models.Model):
    name = models.CharField(max_length=100, blank=False)
    version = models.CharField(max_length=10, blank=False)
    module = models.CharField(max_length=50, default='default')
    platform = models.CharField(max_length=50, blank=True)
    data_analysis_type = models.ForeignKey(OntologyTerm, null=True, related_name="%(app_label)s_%(class)s_data_analysis_type")
    parameter = models.CharField(max_length=200, default='default')
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('name', 'version', 'module', 'parameter',)

    def __unicode__(self):
        return u"""{name}:{version}:{parameter}""".format(
            name=self.name,
            version=self.version,
            parameter=self.parameter,
        )