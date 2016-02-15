# Python imports
import commands, os, string, sys

# Setup environ
import django
sys.path.append('../..')
os.environ['DJANGO_SETTINGS_MODULE'] = "toxomine-staging-database.settings.local"

# Local app imports
import exporter_antibody
import exporter_data_analysis
import exporter_datafile
import exporter_experiment
import exporter_experimental_factor
import exporter_gene
import exporter_lab
import exporter_microarray
import exporter_organism
import exporter_project
import exporter_protocol
import exporter_publication
import exporter_submission
import exporter_toxoplasma_mutant

# Setup django
django.setup()

######################################################################################################
##  Object Loaders
######################################################################################################
def load_data(file_path, url):
    exporter_antibody.export_antibody_items(file_path)
    exporter_data_analysis.export_data_analysis_items(file_path)
    exporter_datafile.export_persistent_datafile_items(file_path, url)
    exporter_datafile.export_submission_datafile_items(file_path, url)
    exporter_experiment.export_experiment_items(file_path)
    exporter_experimental_factor.export_experimental_factor_items(file_path)
    exporter_gene.export_gene_items(file_path)
    exporter_lab.export_lab_items(file_path)
    exporter_microarray.export_microarray_items(file_path)
    exporter_organism.export_organism_items(file_path)
    exporter_project.export_project_items(file_path)
    exporter_protocol.export_protocol_items(file_path)
    exporter_publication.export_publication_items(file_path)
    exporter_submission.export_applied_protocol_items(file_path)
    exporter_submission.export_submission_items(file_path)
    exporter_submission.export_submission_data_items(file_path)
    exporter_toxoplasma_mutant.export_toxoplasma_mutant_items(file_path)

    combine_data(file_path)

######################################################################################################
##  Combine all *-items.xml to create toxocore-items.xml
######################################################################################################
def combine_data(file_path):
    antibody_items = file_path + '/antibody-items.xml'
    applied_protocol_items = file_path + '/applied-protocol-items.xml'
    data_analysis_items = file_path + '/data-analysis-items.xml'
    experiment_items = file_path + '/experiment-items.xml'
    experimental_factor_items = file_path + '/experimental-factor-items.xml'
    gene_items = file_path + '/gene-items.xml'
    lab_items = file_path + '/lab-items.xml'
    microarray_items = file_path + '/microarray-items.xml'
    organism_items = file_path + '/organism-items.xml'
    persistent_datafile_items = file_path + '/persistent-datafile-items.xml'
    project_items = file_path + '/project-items.xml'
    protocol_items = file_path + '/protocol-items.xml'
    publication_items = file_path + '/publication-items.xml'    
    submission_items = file_path + '/submission-items.xml'
    submission_data_items = file_path + '/submissiondata-items.xml'
    submission_datafile_items = file_path + '/submission-datafile-items.xml'
    toxoplasma_mutant_items = file_path + '/toxoplasma-mutant-items.xml'

    output_items = file_path + '/toxomine-staging-database-items.xml'

    cmd = 'cat ' + organism_items + ' ' + gene_items + ' ' + publication_items + ' '  + lab_items + ' ' + \
        project_items + ' ' + experiment_items + ' ' + submission_items + ' ' + \
        protocol_items+ ' ' + applied_protocol_items + ' ' + submission_data_items + ' ' + toxoplasma_mutant_items + ' ' + \
        antibody_items + ' ' + experimental_factor_items + ' ' + microarray_items + ' ' + data_analysis_items + ' ' + \
        persistent_datafile_items + ' ' + submission_datafile_items + ' > ' + output_items
    statusCommands = commands.getstatusoutput(cmd)

    cmd  = "sed -i '1i <items>\n' " + output_items
    statusCommands = commands.getstatusoutput(cmd)
    
    cmd = "echo '</items>' >> " + output_items
    statusCommands = commands.getstatusoutput(cmd)

######################################################################################################
##  Main Program
######################################################################################################
def main():
    if len(sys.argv) > 1:
        try:
            infile = open(sys.argv[1])
            raw = infile.readlines()
            infile.close()

            file_path = string.strip(raw[0])
            url = string.strip(raw[1])

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            load_data(file_path, url)

        except OSError:
            sys.exit('Check arguments - config file not found')
    else:
        sys.exit('Check arguments - config_file')

if __name__=="__main__":
    main()