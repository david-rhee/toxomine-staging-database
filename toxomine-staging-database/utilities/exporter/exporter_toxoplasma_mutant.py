# Python imports

# Core Django imports

# Local app imports
from organisms.models import OrganismProperty
from submissions.models import SubmissionData
from toxoplasmagondiis.models import ToxoplasmaMutant

import exporter_utility

######################################################################################################
##  Export ToxoplasmMutant as InterMine Item
######################################################################################################
def export_toxoplasma_mutant_items(file_path) :
    toxoplasma_mutants = ToxoplasmaMutant.objects.all() # get all objects
    
    if toxoplasma_mutants: # check if empty
        outfile = open(file_path+'/toxoplasma-mutant-items.xml', 'w') # open and write to *-items.xml

        for toxoplasma_mutant in toxoplasma_mutants:
            submission_data_list = SubmissionData.objects.all().filter(object_id=toxoplasma_mutant.id)

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
                outfile.write('<item id="ToxoplasmaMutant_' + str(toxoplasma_mutant.id) + '" class="ToxoplasmaMutant">\n')
                outfile.write('\t<attribute name="name" value="' + toxoplasma_mutant.name + '" />\n')
                outfile.write('\t<attribute name="targetName" value="' + toxoplasma_mutant.target_name + '" />\n')
                outfile.write('\t<attribute name="mutantSelection" value="' + toxoplasma_mutant.selection.name + '" />\n')
                outfile.write('\t<attribute name="mutantType" value="' + toxoplasma_mutant.mutation_type.name + '" />\n')
                outfile.write('\t<attribute name="mutantBackground" value="' + toxoplasma_mutant.background.name + '" />\n')

                strain = ''
                background = ''

                organism_property_list = OrganismProperty.objects.all().filter(organism=toxoplasma_mutant.organism) # organism property
                for organism_property in organism_property_list:
                    if organism_property.organism_property_type.name == 'organism strain':
                        strain = organism_property.organism_property_value.name
                    if organism_property.organism_property_type.name == 'organism type':
                        background = organism_property.organism_property_value.name

                outfile.write('\t<attribute name="strain" value="' + strain + '" />\n')
                outfile.write('\t<attribute name="background" value="' + background + '" />\n')
    
                if toxoplasma_mutant.target_gene:
                    exporter_utility.write_reference_item(outfile, toxoplasma_mutant.target_gene, 'Gene', 'targetGene')
                if toxoplasma_mutant.organism:
                    exporter_utility.write_reference_item(outfile, toxoplasma_mutant.organism, 'Organism', 'organism')
                if project_list:
                    exporter_utility.write_collection_items(outfile, project_list, 'Project', 'projects')
                if experiment_list:
                    exporter_utility.write_collection_items(outfile, experiment_list, 'Experiment', 'experiments')
                if submission_list:
                    exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file