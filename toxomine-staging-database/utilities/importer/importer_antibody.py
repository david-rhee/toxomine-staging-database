# Python imports
import distutils

# Core Django imports
from django.core.exceptions import ValidationError

# Local app imports
from antibodies.models import Antibody

######################################################################################################
##  Get or Create Antibody with target gene
######################################################################################################
def get_antibody_with_target_gene(name, target_name, tagged, tag_target, source, catalog_number, epitope, lot_number, ifa_localization,
                                  chip_peaks, monoclonal, isotype, immunogen_source, conjugation, validated, url, animal_host, target_gene):
    #check if antibody exist, if so return, if not create new
    try:
        
        if animal_host:        
            antibody = Antibody(name=name, target_name=target_name, tagged=distutils.util.strtobool(tagged), tag_target=tag_target, source=source, catalog_number=catalog_number, epitope=epitope, lot_number=lot_number,
                                ifa_localization=ifa_localization, chip_peaks=chip_peaks, monoclonal=monoclonal, isotype=isotype,
                                immunogen_source=immunogen_source, conjugation=conjugation, validated=validated, url=url,
                                animal_host=animal_host, target_gene=target_gene)
        else:
            antibody = Antibody(name=name, target_name=target_name, tagged=distutils.util.strtobool(tagged), tag_target=tag_target, source=source, catalog_number=catalog_number, epitope=epitope, lot_number=lot_number,
                                ifa_localization=ifa_localization, chip_peaks=chip_peaks, monoclonal=monoclonal, isotype=isotype,
                                immunogen_source=immunogen_source, conjugation=conjugation, validated=validated, url=url,
                                target_gene=target_gene)

        antibody.validate_unique()
        antibody.save()

    except ValidationError as e:
        antibody = Antibody.objects.get(name=name, target_name=target_name, tagged=distutils.util.strtobool(tagged), tag_target=tag_target, target_gene=target_gene)

    return antibody

######################################################################################################
##  Get or Create Antibody without target gene
######################################################################################################
def get_antibody_without_target_gene(name, target_name, tagged, tag_target, source, catalog_number, epitope, lot_number, ifa_localization,
                                     chip_peaks, monoclonal, isotype, immunogen_source, conjugation, validated, url, animal_host):
    #check if antibody exist, if so return, if not create new
    try:
        if animal_host:
            antibody = Antibody(name=name, target_name=target_name, tagged=distutils.util.strtobool(tagged), tag_target=tag_target, source=source, catalog_number=catalog_number, epitope=epitope, lot_number=lot_number,
                                ifa_localization=ifa_localization, chip_peaks=chip_peaks, monoclonal=monoclonal, isotype=isotype,
                                immunogen_source=immunogen_source, conjugation=conjugation, validated=validated, url=url,
                                animal_host=animal_host)
        else:
            antibody = Antibody(name=name, target_name=target_name, tagged=distutils.util.strtobool(tagged), tag_target=tag_target, source=source, catalog_number=catalog_number, epitope=epitope, lot_number=lot_number,
                                ifa_localization=ifa_localization, chip_peaks=chip_peaks, monoclonal=monoclonal, isotype=isotype,
                                immunogen_source=immunogen_source, conjugation=conjugation, validated=validated, url=url)

        antibody.validate_unique()
        antibody.save()

    except ValidationError as e:
        antibody = Antibody.objects.get(name=name, target_name=target_name, tagged=distutils.util.strtobool(tagged), tag_target=tag_target)

    return antibody