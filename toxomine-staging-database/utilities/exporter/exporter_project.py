# Python imports

# Core Django imports
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

# Local app imports
from antibodies.models import Antibody
from contacts.models import Lab
from experiments.models import Experiment
from projects.models import Project
from submissions.models import AppliedProtocol, Submission, SubmissionData
from toxoplasmagondiis.models import ToxoplasmaMutant

import exporter_utility

######################################################################################################
##  Export Project as InterMine Item
######################################################################################################
def export_project_items(file_path) :
    projects = Project.objects.all().filter(publishable=True) # get all objects
    
    if projects: # check if empty
        outfile = open(file_path+'/project-items.xml', 'w') # open and write to *-items.xml

        for project in projects:
            publication_list = project.publications.all() # publications

            lab_list = [] # labs
            contributors = project.contributors.all() # Grab all project contributors
            # Grab all the projects by each member of the lab
            for contributor in contributors:
                tmp_list = Lab.objects.all().filter(lab_members=contributor)
                if tmp_list:
                    lab_list.extend(tmp_list)
            lab_list = list(set(lab_list)) # Get rid of duplicates

            experiment_list = Experiment.objects.all().filter(projects=project).filter(publishable=True) # experiments

            submission_list = [] # submissions
            # Grab all the submissions
            for experiment in experiment_list:
                tmp_list = Submission.objects.all().filter(experiments=experiment).filter(publishable=True)
                if tmp_list:
                    submission_list.extend(tmp_list)
            submission_list = list(set(submission_list)) # Get rid of duplicates

            organism_list = [] # organisms
            toxoplasma_mutant_list = [] # toxoplasma mutants
            antibody_list = [] # antibody
            # Grab all the submission data
            for submission in submission_list:                
                applied_protocol_list = AppliedProtocol.objects.all().filter(submission=submission)
                for applied_protocol in applied_protocol_list:
                    submission_data_list = SubmissionData.objects.all().filter(Q(applied_protocol_input=applied_protocol) | Q(applied_protocol_output=applied_protocol))
                    for submission_data in submission_data_list:
                        if submission_data.content_type==ContentType.objects.get_for_model(ToxoplasmaMutant):
                            toxoplasma_mutant_list.append(submission_data.content_object)
                            organism_list.append(submission_data.content_object.organism)
                        if submission_data.content_type==ContentType.objects.get_for_model(Antibody):
                            antibody_list.append(submission_data.content_object)

            organism_list = list(set(organism_list)) # Get rid of duplicates
            toxoplasma_mutant_list = list(set(toxoplasma_mutant_list)) # Get rid of duplicates
            antibody_list = list(set(antibody_list)) # Get rid of duplicates

            # Only export if there is a related objects
            if publication_list or lab_list or experiment_list or submission_list or organism_list or toxoplasma_mutant_list or antibody_list: 
                outfile.write('<item id="Project_' + str(project.id) + '" class="Project">\n')
                outfile.write('\t<attribute name="name" value="' + project.name + '" />\n')
                outfile.write('\t<attribute name="description" value="' + project.description + '" />\n')
                if publication_list:
                    exporter_utility.write_collection_items(outfile, publication_list, 'Publication', 'publications')
                if lab_list:
                    exporter_utility.write_collection_items(outfile, lab_list, 'Lab', 'labs')
                if experiment_list:
                    exporter_utility.write_collection_items(outfile, experiment_list, 'Experiment', 'experiments')
                if submission_list:
                    exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                if organism_list:
                    exporter_utility.write_collection_items(outfile, organism_list, 'Organism', 'organisms')
                if toxoplasma_mutant_list:
                    exporter_utility.write_collection_items(outfile, toxoplasma_mutant_list, 'ToxoplasmaMutant', 'toxoplasmaMutants')
                if antibody_list:
                    exporter_utility.write_collection_items(outfile, antibody_list, 'Antibody', 'antibodies')
                outfile.write('</item>\n')

        outfile.close() # close file