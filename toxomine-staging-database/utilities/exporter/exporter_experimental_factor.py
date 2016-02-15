# Python imports

# Core Django imports

# Local app imports
from experimentalfactors.models import ExperimentalFactor
from submissions.models import Submission, AppliedProtocol, SubmissionData

import exporter_utility

######################################################################################################
##  Export ExperimentalFactor as InterMine Item
######################################################################################################
def export_experimental_factor_items(file_path) :
    experimental_factors = ExperimentalFactor.objects.all() # get all objects
    
    if experimental_factors: # check if empty
        outfile = open(file_path+'/experimental-factor-items.xml', 'w') # open and write to *-items.xml

        for experimental_factor in experimental_factors:
            submission_data_list = SubmissionData.objects.all().filter(object_id=experimental_factor.id)

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

            # Only export if there is a related objects
            if submission_list: 
                outfile.write('<item id="ExperimentalFactor_' + str(experimental_factor.id) + '" class="ExperimentalFactor">\n')
                outfile.write('\t<attribute name="type" value="' + experimental_factor.name.name + '" />\n')
                outfile.write('\t<attribute name="value" value="' + experimental_factor.value + '" />\n')
                exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file