# Python imports

# Core Django imports

# Local app imports
from experiments.models import Experiment
from projects.models import Project
from publications.models import Publication
from submissions.models import Submission

import exporter_utility

######################################################################################################
##  Export Publication as InterMine Item
######################################################################################################
def export_publication_items(file_path) :
    publications = Publication.objects.all() # get all objects

    if publications: # check if empty
        outfile = open(file_path+'/publication-items.xml', 'w') # open and write to *-items.xml

        for publication in publications:
            dbxrefs_list = publication.dbxrefs.all() # dbxrefs
            for dbxref in dbxrefs_list:
                if dbxref.db.name == 'Pubmed':
                    pubmed_id = dbxref.accession
            
            project_list = Project.objects.all().filter(publications=publication).filter(publishable=True)
            experiment_list = Experiment.objects.all().filter(publications=publication).filter(publishable=True)
            submission_list = Submission.objects.all().filter(publications=publication).filter(publishable=True)
            
            # Only export if there is a related objects
            if pubmed_id and (project_list or experiment_list or submission_list): 
                outfile.write('<item id="Publication_' + str(publication.id) + '" class="Publication">\n')
                outfile.write('\t<attribute name="pubMedId" value="' + str(pubmed_id) + '" />\n')
                outfile.write('\t<attribute name="title" value="' + str(publication.unique_name) + '" />\n')
                if project_list:
                    exporter_utility.write_collection_items(outfile, project_list, 'Project', 'projects')
                if experiment_list:
                    exporter_utility.write_collection_items(outfile, experiment_list, 'Experiment', 'experiments')
                if submission_list:
                    exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')
        
        outfile.close() # close file