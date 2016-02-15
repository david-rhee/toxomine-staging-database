# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from general.models import Dbxref

#####################################################################################################
#  Based on Chado's controlled vocabulary module
#  Ontology = Controlled Vocabulary
#####################################################################################################

#####################################################################################################
#  Ontology
"""
 An ontology is composed of ontology terms (AKA terms, classes, types, universals - relations and properties are also stored in ontologyterm)
 and the relationships between them.
"""
class Ontology(models.Model):
    name = models.CharField(max_length=255, unique=True)
    definition = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)

#####################################################################################################
#  OntologyTermType
"""
 A term type within an ontology. This table is used for relations and properties.
 OntologyTermTypes constitute edges in the graph defined by the collection of OntologyTerm, OntologyTermType and OntologyTermRelationship.
"""
class OntologyTermType(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    definition = models.TextField(blank=True)
    obsolete = models.BooleanField(default=False) # Note that two terms with different primary dbxrefs may exist if one is obsolete.
    #Relationships
    ontology = models.ForeignKey(Ontology, null=False, related_name="%(app_label)s_%(class)s_ontology")

    class Meta:
        unique_together = ('name', 'ontology')
        ordering = ['ontology', 'name']

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)

#####################################################################################################
#  OntologyTerm
"""
 A term, class or universal within an ontology.
 OntologyTerms constitute nodes in the graph defined by the collection of OntologyTerm, OntologyTermType and OntologyTermRelationship.
"""
class OntologyTerm(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    definition = models.TextField(blank=True)
    obsolete = models.BooleanField(default=False) # Note that two terms with different primary dbxrefs may exist if one is obsolete.
    #Relationships
    related_ontology_terms = models.ManyToManyField('self', through='OntologyTermM2M', symmetrical=False, related_name='%(app_label)s_%(class)s_related_ontology_terms')
    ontology = models.ForeignKey(Ontology, null=False, related_name="%(app_label)s_%(class)s_ontology")

    class Meta:
        unique_together = ('name', 'definition', 'ontology')
        ordering = ['ontology', 'name']

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)

    def get_parents(self, ontology_term_type):
        return self.related_ontology_terms.filter(ontologies_ontologytermm2m_ontology_term_parent__ontology_term_type__name=ontology_term_type,
                                                  ontologies_ontologytermm2m_ontology_term_parent__ontology_term_child=self)
    
    def get_childs(self, ontology_term_type):
        return self.related_ontology_terms.filter(ontologies_ontologytermm2m_ontology_term_child__ontology_term_type__name=ontology_term_type,
                                                  ontologies_ontologytermm2m_ontology_term_child__ontology_term_parent=self)

"""
 A relationship linking two OntologyTerms and corresponding OntologyTermType.
 <child term> <type> <parent term>
""" 
class OntologyTermM2M(models.Model):
    ontology_term_type = models.ForeignKey(OntologyTermType, null=False, related_name="%(app_label)s_%(class)s_ontology_term_type")
    ontology_term_parent = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_ontology_term_parent")
    ontology_term_child = models.ForeignKey(OntologyTerm, null=False, related_name="%(app_label)s_%(class)s_ontology_term_child")
    ontology = models.ForeignKey(Ontology, null=True, related_name="%(app_label)s_%(class)s_ontology") # If the closure of a relationship traverses an ontology then this refers to the ontology of the parent ontology term.
    path_distance = models.IntegerField(default=0)

    class Meta:
        unique_together = ('path_distance', 'ontology_term_type', 'ontology_term_parent', 'ontology_term_child')

    def __unicode__(self):
        return u"""{ontology_term_child} {ontology_term_type} {ontology_term_parent}""".format(
            ontology_term_parent=self.ontology_term_parent,
            ontology_term_type=self.ontology_term_type,
            ontology_term_child=self.ontology_term_child,
        )