# Python imports

# Core Django imports
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

# Local app imports
from antibodies.models import Antibody
from dataanalyses.models import DataAnalysis
from datafiles.models import PersistentDataFile, SubmissionDataFile
from experimentalfactors.models import ExperimentalFactor
from contacts.models import Lab
from microarrays.models import MicroArray
from sequencings.models import Sequencing
from submissions.models import AppliedProtocol, Submission, SubmissionData
from toxoplasmagondiis.models import ToxoplasmaMutant

import exporter_utility

######################################################################################################
##  Export Submission as InterMine Item
######################################################################################################
def export_submission_items(file_path) :
    submissions = Submission.objects.all().filter(publishable=True) # get all objects
    
    if submissions: # check if empty
        outfile = open(file_path+'/submission-items.xml', 'w') # open and write to *-items.xml

        for submission in submissions:
            publication_list = submission.publications.all() # publications

            lab_list = [] # labs
            contributors = submission.contributors.all() # Grab all submission contributors
            # Grab all the submission by each member of the lab
            for contributor in contributors:
                tmp_list = Lab.objects.all().filter(lab_members=contributor)
                if tmp_list:
                    lab_list.extend(tmp_list)
            lab_list = list(set(lab_list)) # Get rid of duplicates

            experiment_list = submission.experiments.all().filter(publishable=True) # experiments

            project_list = [] # projects
            for experiment in experiment_list:
                tmp_list = experiment.projects.all().filter(publishable=True)
                project_list.extend(tmp_list)
            project_list = list(set(project_list)) # Get rid of duplicates

            applied_protocol_list = [] # applied protocols
            protocol_list = [] # protocols
            organism_list = [] # organisms
            toxoplasma_mutant_list = [] # toxoplasma mutants
            antibody_list = [] # antibodies
            experimental_factor_list = [] # experimental factor
            microarray_list = [] # microarray
            sequencing_list = [] # sequencing
            data_analysis_list = [] # data analysis
            persistent_datafile_list = [] # persistent datafile
            submission_datafile_list = [] # submission datafile

            # Grab all the organisms and toxoplasma mutants
            applied_protocol_list = AppliedProtocol.objects.all().filter(submission=submission)
            for applied_protocol in applied_protocol_list:
                protocol_list.append(applied_protocol.protocol) # protocols
                submission_data_list = SubmissionData.objects.all().filter(Q(applied_protocol_input=applied_protocol) | Q(applied_protocol_output=applied_protocol))
                for submission_data in submission_data_list:
                    if submission_data.content_type==ContentType.objects.get_for_model(ToxoplasmaMutant):
                        toxoplasma_mutant_list.append(submission_data.content_object)
                        organism_list.append(submission_data.content_object.organism)
                    if submission_data.content_type==ContentType.objects.get_for_model(Antibody):
                        antibody_list.append(submission_data.content_object)
                    if submission_data.content_type==ContentType.objects.get_for_model(ExperimentalFactor):
                        experimental_factor_list.append(submission_data.content_object)
                    if submission_data.content_type==ContentType.objects.get_for_model(MicroArray):
                        microarray_list.append(submission_data.content_object)
                    if submission_data.content_type==ContentType.objects.get_for_model(Sequencing):
                        sequencing_list.append(submission_data.content_object)
                    if submission_data.content_type==ContentType.objects.get_for_model(DataAnalysis):
                        data_analysis_list.append(submission_data.content_object)                        
                    if submission_data.content_type==ContentType.objects.get_for_model(PersistentDataFile):
                        persistent_datafile_list.append(submission_data.content_object)
                    if submission_data.content_type==ContentType.objects.get_for_model(SubmissionDataFile):
                        submission_datafile_list.append(submission_data.content_object)

            protocol_list = list(set(protocol_list)) # Get rid of duplicates
            organism_list = list(set(organism_list)) # Get rid of duplicates
            toxoplasma_mutant_list = list(set(toxoplasma_mutant_list)) # Get rid of duplicates
            antibody_list = list(set(antibody_list)) # Get rid of duplicates
            experimental_factor_list = list(set(experimental_factor_list)) # Get rid of duplicates
            microarray_list = list(set(microarray_list)) # Get rid of duplicates
            sequencing_list = list(set(sequencing_list)) # Get rid of duplicates
            data_analysis_list = list(set(data_analysis_list)) # Get rid of duplicates
            persistent_datafile_list = list(set(persistent_datafile_list)) # Get rid of duplicates
            submission_datafile_list = list(set(submission_datafile_list)) # Get rid of duplicates

            # Only export if there is a related labs
            if publication_list or lab_list or project_list or experiment_list or applied_protocol_list or protocol_list:

                outfile.write('<item id="Submission_' + str(submission.id) + '" class="Submission">\n')
                outfile.write('\t<attribute name="TCid" value="' + submission.generated_id + '" />\n')
                outfile.write('\t<attribute name="name" value="' + submission.name + '" />\n')
                outfile.write('\t<attribute name="description" value="' + submission.description + '" />\n')
                outfile.write('\t<attribute name="technique" value="' + submission.technique.name + '" />\n')
                outfile.write('\t<attribute name="qualityControl" value="' + submission.quality_control.name + '" />\n')
                outfile.write('\t<attribute name="embargoDate" value="' + str(submission.date_embargo) + '" />\n')
                outfile.write('\t<attribute name="publicReleaseDate" value="' + str(submission.date_created) + '" />\n')
                outfile.write('\t<attribute name="replicateDate" value="' + str(submission.date_replicate) + '" />\n')

                if publication_list:
                    exporter_utility.write_collection_items(outfile, publication_list, 'Publication', 'publications')
                if lab_list:
                    exporter_utility.write_collection_items(outfile, lab_list, 'Lab', 'labs')
                if project_list:
                    exporter_utility.write_collection_items(outfile, project_list, 'Project', 'projects')
                if experiment_list:
                    exporter_utility.write_collection_items(outfile, experiment_list, 'Experiment', 'experiments')

                if applied_protocol_list:
                    exporter_utility.write_collection_items(outfile, applied_protocol_list, 'AppliedProtocol', 'appliedProtocols')                    
                if protocol_list:
                    exporter_utility.write_collection_items(outfile, protocol_list, 'Protocol', 'protocols')  
                if organism_list:
                    exporter_utility.write_collection_items(outfile, organism_list, 'Organism', 'organisms')
                if toxoplasma_mutant_list:
                    exporter_utility.write_collection_items(outfile, toxoplasma_mutant_list, 'ToxoplasmaMutant', 'toxoplasmaMutants')
                if antibody_list:
                    exporter_utility.write_collection_items(outfile, antibody_list, 'Antibody', 'antibodies')
                if experimental_factor_list:
                    exporter_utility.write_collection_items(outfile, experimental_factor_list, 'ExperimentalFactor', 'experimentalFactors')
                if microarray_list:
                    exporter_utility.write_collection_items(outfile, microarray_list, 'MicroArray', 'microArrays')
                if sequencing_list:
                    exporter_utility.write_collection_items(outfile, sequencing_list, 'Sequencing', 'sequencings')
                if data_analysis_list:
                    exporter_utility.write_collection_items(outfile, data_analysis_list, 'DataAnalysis', 'dataAnalyses')
                if persistent_datafile_list:
                    exporter_utility.write_collection_items(outfile, persistent_datafile_list, 'PersistentDataFile', 'persistentDataFiles')
                if submission_datafile_list:
                    exporter_utility.write_collection_items(outfile, submission_datafile_list, 'SubmissionDataFile', 'submissionDataFiles')
                outfile.write('</item>\n')

        outfile.close() # close file

######################################################################################################
##  Export AppliedProtocol as InterMine Item
######################################################################################################
def export_applied_protocol_items(file_path) :
    applied_protocols = AppliedProtocol.objects.all() # get all objects
    
    if applied_protocols: # check if empty
        outfile = open(file_path+'/applied-protocol-items.xml', 'w') # open and write to *-items.xml

        for applied_protocol in applied_protocols:

            input_list = SubmissionData.objects.all().filter(applied_protocol_input=applied_protocol) # submission data
            output_list = SubmissionData.objects.all().filter(applied_protocol_output=applied_protocol) # submission data
            input_list = list(set(input_list)) # Get rid of duplicates
            output_list = list(set(output_list)) # Get rid of duplicates

            outfile.write('<item id="AppliedProtocol_' + str(applied_protocol.id) + '" class="AppliedProtocol">\n')
            outfile.write('\t<attribute name="step" value="' + str(applied_protocol.step) + '" />\n')
            exporter_utility.write_reference_item(outfile, applied_protocol.protocol, 'Protocol', 'protocol')
            exporter_utility.write_reference_item(outfile, applied_protocol.submission, 'Submission', 'submission')
            if input_list:
                exporter_utility.write_collection_items(outfile, input_list, 'SubmissionData', 'inputs')
            if output_list:
                exporter_utility.write_collection_items(outfile, output_list, 'SubmissionData', 'outputs')
            outfile.write('</item>\n')

        outfile.close() # close file

######################################################################################################
##  Export SubmissionData as InterMine Item
######################################################################################################
def export_submission_data_items(file_path) :
    submission_data = SubmissionData.objects.all() # get all objects
    
    if submission_data: # check if empty
        outfile = open(file_path+'/submissiondata-items.xml', 'w') # open and write to *-items.xml

        for submission_data_singleton in submission_data:
            outfile.write('<item id="SubmissionData_' + str(submission_data_singleton.id) + '" class="SubmissionData">\n')
            outfile.write('\t<attribute name="series" value="' + str(submission_data_singleton.series) + '" />\n')
            outfile.write('\t<attribute name="partOf" value="na" />\n')
            if submission_data_singleton.applied_protocol_input:
                exporter_utility.write_reference_item(outfile, submission_data_singleton.applied_protocol_input, 'AppliedProtocol', 'inputAppliedProtocol')
            if submission_data_singleton.applied_protocol_output:
                exporter_utility.write_reference_item(outfile, submission_data_singleton.applied_protocol_output, 'AppliedProtocol', 'outputAppliedProtocol')

            if submission_data_singleton.content_type==ContentType.objects.get_for_model(ToxoplasmaMutant):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'ToxoplasmaMutant', 'toxoplasmaMutant')
            if submission_data_singleton.content_type==ContentType.objects.get_for_model(Antibody):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'Antibody', 'antibody')
            if submission_data_singleton.content_type==ContentType.objects.get_for_model(ExperimentalFactor):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'ExperimentalFactor', 'experimentalFactor')
            if submission_data_singleton.content_type==ContentType.objects.get_for_model(MicroArray):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'MicroArray', 'microArray')
            if submission_data_singleton.content_type==ContentType.objects.get_for_model(Sequencing):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'Sequencing', 'sequencing')
            if submission_data_singleton.content_type==ContentType.objects.get_for_model(DataAnalysis):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'DataAnalysis', 'dataAnalysis')
            if submission_data_singleton.content_type==ContentType.objects.get_for_model(PersistentDataFile):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'PersistentDataFile', 'persistentDataFile')
            if submission_data_singleton.content_type==ContentType.objects.get_for_model(SubmissionDataFile):
                exporter_utility.write_reference_item(outfile, submission_data_singleton.content_object, 'SubmissionDataFile', 'submissionDataFile')

            outfile.write('</item>\n')

        outfile.close() # close file