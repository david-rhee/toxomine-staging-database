# Python imports
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

# Local app imports
from submissions.models import AppliedProtocol, Submission, SubmissionContributor, SubmissionData

from antibodies.models import Antibody
from dataanalyses.models import DataAnalysis
from datafiles.models import PersistentDataFile
from datafiles.models import SubmissionDataFile
from experimentalfactors.models import ExperimentalFactor
from microarrays.models import MicroArray
from sequencings.models import Sequencing
from toxoplasmagondiis.models import ToxoplasmaMutant

#######################################################################################################################################
#######################################################################################################################################
# Submission
#######################################################################################################################################
def return_unique_generated_id(count):
    return 'TC' + str(count+1)

def return_unique_submission_name(generated_id, given_name):
    return generated_id + '_' + given_name

def get_submission(given_name, description, technique, quality_control, replicate_series, date_replicate, note, publishable, user, experiment, publication_list):
    #check if submission exist, if so return, if not create new
    try:
        year_later = datetime.now() + timedelta(days=(1*365))
        #Get generated id and unique name
        generated_id = return_unique_generated_id(Submission.objects.all().count())
        name = return_unique_submission_name(generated_id, given_name)

        submission = Submission(generated_id=generated_id, name=name, given_name=given_name, description=description,
                                               publishable=publishable, date_created=datetime.now(), date_embargo=year_later,
                                               technique=technique, quality_control=quality_control, replicate_series=replicate_series,
                                               date_replicate=date_replicate, note=note)
        submission.validate_unique() 
        submission.save()
        
        submission.experiments.add(experiment)
        for publication in publication_list:
            submission.publications.add(publication)

        #Establish User to Submission relationships
        submission_contributor = SubmissionContributor.submission_contributor_objects.create_submission_as_superuser(submission, user)
        submission_contributor.validate_unique()
        submission_contributor.save()

    except ValidationError as e:
        print e
        submission = Submission.objects.get(given_name=given_name)
  
    return submission

def add_submission_contributor(submission, user):
    try:
        submission_contributor = SubmissionContributor(submission=submission, user=user, super_user='True', date_joined=datetime.now())
        submission_contributor.validate_unique()
        submission_contributor.save()

    except ValidationError as e:
        submission_contributor = SubmissionContributor.objects.get(submission=submission, user=user)

    return submission_contributor

#######################################################################################################################################
#######################################################################################################################################
# Applied Protocol
#######################################################################################################################################
def get_applied_protocol_start_node(step, protocol, submission):
    applied_protocol = AppliedProtocol(step=step, protocol=protocol, submission=submission)
    applied_protocol.validate_unique()
    applied_protocol.save()
    
    return applied_protocol

def get_applied_protocol_other_node(step, protocol, submission, previous_applied_protocol):
    applied_protocol = AppliedProtocol(step=step, protocol=protocol, submission=submission, previous_applied_protocol=previous_applied_protocol)
    applied_protocol.validate_unique()
    applied_protocol.save()
    
    return applied_protocol

#######################################################################################################################################
#######################################################################################################################################
# Submission Data
#######################################################################################################################################
def get_antibody_submission_data(tmp_holder, antibody_list, applied_protocol, submission_property):
    tmp, first, second, third = tmp_holder.split('<')

    antibody = antibody_list[int(third)-1]
    if first == 'I':
        antibody_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                  content_type=ContentType.objects.get_for_model(Antibody),
                                                  object_id=antibody.id)
    if first == 'O':
        antibody_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                  content_type=ContentType.objects.get_for_model(Antibody),
                                                  object_id=antibody.id)
    antibody_submission_data.save()

def get_data_analysis_submission_data(tmp_holder, data_analysis_list, applied_protocol, submission_property):
    tmp, first, second, third = tmp_holder.split('<')

    data_analysis = data_analysis_list[int(third)-1]
    if first == 'I':
        data_analysis_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                       content_type=ContentType.objects.get_for_model(DataAnalysis),
                                                       object_id=data_analysis.id)
    if first == 'O':
        data_analysis_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                       content_type=ContentType.objects.get_for_model(DataAnalysis),
                                                       object_id=data_analysis.id)
    data_analysis_submission_data.save()

def get_experimental_factor_submission_data(tmp_holder, experimental_factor_list, applied_protocol, submission_property):
    tmp, first, second, third = tmp_holder.split('<')

    experimental_factor = experimental_factor_list[int(third)-1]
    if first == 'I':
        experimental_factor_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                             content_type=ContentType.objects.get_for_model(ExperimentalFactor),
                                                             object_id=experimental_factor.id)
    if first == 'O':
        experimental_factor_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                             content_type=ContentType.objects.get_for_model(ExperimentalFactor),
                                                             object_id=experimental_factor.id)
    experimental_factor_submission_data.save()

def get_microarray_submission_data(tmp_holder, microarray_list, applied_protocol, submission_property):
    tmp, first, second, third = tmp_holder.split('<')

    microarray = microarray_list[int(third)-1]
    if first == 'I':
        microarray_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                    content_type=ContentType.objects.get_for_model(MicroArray),
                                                    object_id=microarray.id)
    if first == 'O':
        microarray_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                    content_type=ContentType.objects.get_for_model(MicroArray),
                                                    object_id=microarray.id)
    microarray_submission_data.save()

def get_sequencing_submission_data(tmp_holder, sequencing_list, applied_protocol, submission_property):
    tmp, first, second, third = tmp_holder.split('<')

    sequencing = sequencing_list[int(third)-1]
    if first == 'I':
        sequencing_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                    content_type=ContentType.objects.get_for_model(Sequencing),
                                                    object_id=sequencing.id)
    if first == 'O':
        sequencing_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                    content_type=ContentType.objects.get_for_model(Sequencing),
                                                    object_id=sequencing.id)
    sequencing_submission_data.save()

def get_persistent_datafile_submission_data(tmp_holder, persistent_datafile_list, applied_protocol, submission_property):
    tmp, first, second, third = tmp_holder.split('<')

    persistent_datafile = persistent_datafile_list[int(third)-1]
    if first == 'I':
        persistent_datafile_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                             content_type=ContentType.objects.get_for_model(PersistentDataFile),
                                                             object_id=persistent_datafile.id)
    if first == 'O':
        persistent_datafile_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                             content_type=ContentType.objects.get_for_model(PersistentDataFile),
                                                             object_id=persistent_datafile.id)
    persistent_datafile_submission_data.save()

def get_submission_datafile_submission_data(tmp_holder, submission_datafile_list, applied_protocol, submission_property):
    tmp, first, second, third = tmp_holder.split('<')

    submission_datafile = submission_datafile_list[int(third)-1]
    if first == 'I':
        submission_datafile_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                             content_type=ContentType.objects.get_for_model(SubmissionDataFile),
                                                             object_id=submission_datafile.id)
    if first == 'O':
        submission_datafile_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                             content_type=ContentType.objects.get_for_model(SubmissionDataFile),
                                                             object_id=submission_datafile.id)
    submission_datafile_submission_data.save()

def get_toxoplasma_mutant_submission_data(tmp_holder, toxoplasma_mutant_list, applied_protocol, submission_property):   
    tmp, first, second, third = tmp_holder.split('<')

    toxoplasma_mutant = toxoplasma_mutant_list[int(third)-1]
    if first == 'I':
        toxoplasma_mutant_submission_data = SubmissionData(series=second, applied_protocol_input=applied_protocol,
                                                           content_type=ContentType.objects.get_for_model(ToxoplasmaMutant),
                                                           object_id=toxoplasma_mutant.id)
    if first == 'O':
        toxoplasma_mutant_submission_data = SubmissionData(series=second, applied_protocol_output=applied_protocol,
                                                           content_type=ContentType.objects.get_for_model(ToxoplasmaMutant),
                                                           object_id=toxoplasma_mutant.id)
    toxoplasma_mutant_submission_data.save()