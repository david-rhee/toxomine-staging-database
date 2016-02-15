# Python imports

# Core Django imports

# Local app imports
from antibodies.models import Antibody
from submissions.models import Submission, AppliedProtocol, SubmissionData

import exporter_utility

######################################################################################################
##  Export Antibody as InterMine Item
######################################################################################################
def export_antibody_items(file_path) :
    antibodies = Antibody.objects.all() # get all objects
    
    if antibodies: # check if empty
        outfile = open(file_path+'/antibody-items.xml', 'w') # open and write to *-items.xml

        for antibody in antibodies:
            submission_data_list = SubmissionData.objects.all().filter(object_id=antibody.id)

            submission_list = [] # submissions
            for submission_data in submission_data_list:
                applied_protocol_list = []
                if submission_data.applied_protocol_input:
                    applied_protocol_list.append(submission_data.applied_protocol_input)
                if submission_data.applied_protocol_output:
                    applied_protocol_list.append(submission_data.applied_protocol_output)                
                
                for applied_protocol in applied_protocol_list:
                    if applied_protocol.submission.publishable == True:
                        submission_list.append(applied_protocol.submission)
            submission_list = list(set(submission_list)) # Get rid of duplicates

            experiment_list = [] # experiment
            for submission in submission_list:
                experiment_list.extend(submission.experiments.all().filter(publishable=True)) # experiments
            experiment_list = list(set(experiment_list)) # Get rid of duplicates

            project_list = [] # projects
            for experiment in experiment_list:
                project_list.extend(experiment.projects.all().filter(publishable=True))
            project_list = list(set(project_list)) # Get rid of duplicates

            # Only export if there is a related objects
            if submission_data_list or project_list or experiment_list or submission_list: 
                outfile.write('<item id="Antibody_' + str(antibody.id) + '" class="Antibody">\n')
                outfile.write('\t<attribute name="name" value="' + antibody.name + '" />\n')
                outfile.write('\t<attribute name="targetName" value="' + antibody.target_name + '" />\n')
                outfile.write('\t<attribute name="source" value="' + antibody.source + '" />\n')
                outfile.write('\t<attribute name="epitope" value="' + antibody.epitope + '" />\n')
                if antibody.animal_host:
                    outfile.write('\t<attribute name="hostOrganism" value="' + antibody.animal_host.name + '" />\n')
                else:
                    outfile.write('\t<attribute name="hostOrganism" value="" />\n')

                if antibody.target_gene:
                    exporter_utility.write_reference_item(outfile, antibody.target_gene, 'Gene', 'targetGene')
                if project_list:
                    exporter_utility.write_collection_items(outfile, project_list, 'Project', 'projects')
                if experiment_list:
                    exporter_utility.write_collection_items(outfile, experiment_list, 'Experiment', 'experiments')
                if submission_list:
                    exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file