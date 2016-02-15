# Python imports

# Core Django imports
from django.core.exceptions import ObjectDoesNotExist

# Local app imports
from ontologies.models import OntologyTerm

######################################################################################################
##  Get Ontology Term
######################################################################################################
def get_ontology_term(class_name, field_name, field_value):
    try:
        ontology_term_value = OntologyTerm.objects.get(
                                ontologies_ontologytermm2m_ontology_term_child__ontology_term_child__name__exact=field_value,
                                ontologies_ontologytermm2m_ontology_term_child__ontology_term_parent__name__exact=field_name,
                                ontologies_ontologytermm2m_ontology_term_child__ontology_term_parent__ontologies_ontologytermm2m_ontology_term_child__ontology_term_parent__name__exact=class_name)

    except OntologyTerm.DoesNotExist:
        sys.exit('Ontology term does not exist')
   
    return ontology_term_value