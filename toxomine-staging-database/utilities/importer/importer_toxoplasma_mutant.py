# Python imports

# Core Django imports
from django.core.exceptions import ValidationError

# Local app imports
from toxoplasmagondiis.models import ToxoplasmaMutant

######################################################################################################
##  Get or Create Toxoplasma Mutant with target gene
######################################################################################################
def get_toxoplasma_mutant_with_target_gene(name, target_name, background, selection, mutation_type, promoter, organism, target_gene):
    #check if toxoplasma mutant exist, if so return, if not create new
    try:
        toxoplasma_mutant = ToxoplasmaMutant(name=name, target_name=target_name, background=background, selection=selection,
                                             mutation_type=mutation_type, promoter=promoter, organism=organism, target_gene=target_gene)
        toxoplasma_mutant.validate_unique()
        toxoplasma_mutant.save()

    except ValidationError as e:
        toxoplasma_mutant = ToxoplasmaMutant.objects.get(name=name, target_name=target_name, background=background, selection=selection,
                                                         mutation_type=mutation_type, promoter=promoter, organism=organism, target_gene=target_gene)
    
    return toxoplasma_mutant

######################################################################################################
##  Get or Create Toxoplasma Mutant without target gene
######################################################################################################
def get_toxoplasma_mutant_without_target_gene(name, target_name, background, selection, mutation_type, promoter, organism):
    #check if toxoplasma mutant exist, if so return, if not create new
    try:
        toxoplasma_mutant = ToxoplasmaMutant(name=name, target_name=target_name, background=background, selection=selection,
                                             mutation_type=mutation_type, promoter=promoter, organism=organism)
        toxoplasma_mutant.validate_unique()
        toxoplasma_mutant.save()

    except ValidationError as e:
        toxoplasma_mutant = ToxoplasmaMutant.objects.get(name=name, target_name=target_name, background=background, selection=selection,
                                                         mutation_type=mutation_type, promoter=promoter, organism=organism)
    
    return toxoplasma_mutant