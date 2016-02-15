# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from organisms.models import Organism

#####################################################################################################
#  Based on Chado's sequence module
#  For now, not based on Chado's sequence module
#  Annotation & Chromosome & Gene<Feature> --- Need to fix this later
######################################################################################################
"""
Class to hold Annotation information
"""
class Annotation(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Annotation name')
    source = models.CharField(max_length=255, null=False, blank=False)
    version = models.CharField(max_length=10, null=False, blank=False)
    #Relationships
    organism = models.ForeignKey(Organism, null=False, blank=False)

    class Meta:
        unique_together = ('name', 'source', 'version')

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)

"""
Class to hold Chromosome information
"""
class Chromosome(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    #Relationships
    annotation = models.ForeignKey(Annotation)

    class Meta:
        unique_together = ('name', 'annotation')

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)

"""
Class to hold Gene information
"""
class Gene(models.Model):
    gene_id = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, blank=True)
    alias = models.CharField(max_length=255, blank=True)
    size = models.IntegerField(blank=True)
    location_start = models.IntegerField(blank=True)
    location_end = models.IntegerField(blank=True)
    strand = models.CharField(max_length=2)
    #Relationships
    annotation = models.ForeignKey(Annotation)
    chromosome = models.ForeignKey(Chromosome)

    def __unicode__(self):
        return u"""{name}""".format(gene_id=self.gene_id)