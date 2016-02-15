# Python imports

# Core Django imports

# Local app imports
from contacts.models import Lab
from experiments.models import Experiment
from projects.models import Project
from submissions.models import Submission

import exporter_utility

######################################################################################################
##  Export Lab as InterMine Item
######################################################################################################
def export_lab_items(file_path) :
    labs = Lab.objects.all() # get all lab objects
    
    if labs: # check if empty
        outfile = open(file_path+'/lab-items.xml', 'w') # open and write to *-items.xml

        for lab in labs:
            lab_members = lab.lab_members.all() # Grab all lab members
            
            project_list = [] # projects
            experiment_list = [] # experiments
            submission_list = [] # submissions
            
            # For each member of the lab
            for lab_member in lab_members:
                tmp_project_list = Project.objects.all().filter(contributors=lab_member).filter(publishable=True)
                if tmp_project_list:
                    project_list.extend(tmp_project_list)
                tmp_experiment_list = Experiment.objects.all().filter(contributors=lab_member).filter(publishable=True)
                if tmp_experiment_list:
                    experiment_list.extend(tmp_experiment_list)                    
                tmp_submission_list = Submission.objects.all().filter(contributors=lab_member).filter(publishable=True)
                if tmp_submission_list:
                    submission_list.extend(tmp_submission_list)                    

            project_list = list(set(project_list)) # Get rid of duplicates
            experiment_list = list(set(experiment_list)) # Get rid of duplicates
            submission_list = list(set(submission_list)) # Get rid of duplicates

            # Only export if there is a related objects
            if project_list or experiment_list or submission_list: 
                outfile.write('<item id="Lab_' + str(lab.id) + '" class="Lab">\n')
                outfile.write('\t<attribute name="name" value="' + lab.name + '" />\n')
                outfile.write('\t<attribute name="piFirstName" value="' + lab.pi_first_name + '" />\n')
                outfile.write('\t<attribute name="piLastName" value="' + lab.pi_last_name + '" />\n')
                outfile.write('\t<attribute name="affiliation" value="' + lab.affiliation + '" />\n')
                if project_list:
                    exporter_utility.write_collection_items(outfile, project_list, 'Project', 'projects')
                if experiment_list:
                    exporter_utility.write_collection_items(outfile, experiment_list, 'Experiment', 'experiments')
                if submission_list:
                    exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file