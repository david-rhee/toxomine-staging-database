# Python imports

# Core Django imports
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

# Local app imports
from antibodies.models import Antibody
from experiments.models import Experiment
from contacts.models import Lab
from submissions.models import Submission, AppliedProtocol, SubmissionData
from toxoplasmagondiis.models import ToxoplasmaMutant

import exporter_utility

######################################################################################################
##  Export Experiment as InterMine Item
######################################################################################################
def export_experiment_items(file_path) :
    experiments = Experiment.objects.all().filter(publishable=True) # get all objects
    
    if experiments: # check if empty
        outfile = open(file_path+'/experiment-items.xml', 'w') # open and write to *-items.xml

        for experiment in experiments:
            publication_list = experiment.publications.all() # publications

            lab_list = [] # labs
            contributors = experiment.contributors.all() # Grab all experiment contributors
            # Grab all the experiments by each member of the lab
            for contributor in contributors:
                tmp_list = Lab.objects.all().filter(lab_members=contributor)
                if tmp_list:
                    lab_list.extend(tmp_list)
            lab_list = list(set(lab_list)) # Get rid of duplicates

            project_list = experiment.projects.all().filter(publishable=True) # projects
            submission_list = Submission.objects.all().filter(experiments=experiment).filter(publishable=True) # submissions

            organism_list = [] # organisms
            toxoplasma_mutant_list = [] # toxoplasma mutants
            antibody_list = [] # antibodies

            # Grab all the organisms and toxoplasma mutants
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

            # Only export if there is a related labs
            if publication_list or lab_list or project_list or submission_list or organism_list or toxoplasma_mutant_list or antibody_list: 
                outfile.write('<item id="Experiment_' + str(experiment.id) + '" class="Experiment">\n')
                outfile.write('\t<attribute name="name" value="' + experiment.name + '" />\n')
                outfile.write('\t<attribute name="description" value="' + experiment.description + '" />\n')
                outfile.write('\t<attribute name="category" value="' + experiment.category.name + '" />\n')
                if publication_list:
                    exporter_utility.write_collection_items(outfile, publication_list, 'Publication', 'publications')
                if lab_list:
                    exporter_utility.write_collection_items(outfile, lab_list, 'Lab', 'labs')
                if project_list:
                    exporter_utility.write_collection_items(outfile, project_list, 'Project', 'projects')
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