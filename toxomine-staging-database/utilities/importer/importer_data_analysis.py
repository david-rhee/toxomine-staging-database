# Python imports

# Core Django imports
from django.core.exceptions import ValidationError

# Local app imports
from dataanalyses.models import DataAnalysis

######################################################################################################
##  Get or Create DataAnalysis
######################################################################################################
def get_data_analysis(name, version, module, platform, data_analysis_type, parameter, notes):
    #check if data_analysis, if so return, if not create new
    try:
        data_analysis = DataAnalysis(name=name, version=version, module=module, platform=platform, data_analysis_type=data_analysis_type, parameter=parameter, notes=notes)
        data_analysis.validate_unique()
        data_analysis.save()

    except ValidationError as e:
        data_analysis = DataAnalysis.objects.get(name=name, version=version, module=module, parameter=parameter)
    
    return data_analysis