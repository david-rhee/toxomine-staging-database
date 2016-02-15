# Python imports

# Core Django imports

# Local app imports
from microarrays.models import MicroArray
from submissions.models import Submission, AppliedProtocol, SubmissionData

import exporter_utility

######################################################################################################
##  Export MicroArray as InterMine Item
######################################################################################################
def export_microarray_items(file_path) :
    microarrays = MicroArray.objects.all() # get all objects
    
    if microarrays: # check if empty
        outfile = open(file_path+'/microarray-items.xml', 'w') # open and write to *-items.xml

        for microarray in microarrays:
            submission_data_list = SubmissionData.objects.all().filter(object_id=microarray.id)

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
                outfile.write('<item id="MicroArray_' + str(microarray.id) + '" class="MicroArray">\n')
                outfile.write('\t<attribute name="name" value="' + microarray.name + '" />\n')
                outfile.write('\t<attribute name="platform" value="' + microarray.platform.name + '" />\n')
                outfile.write('\t<attribute name="format" value="' + microarray.microarray_format.name + '" />\n')
                outfile.write('\t<attribute name="version" value="' + microarray.version + '" />\n')
                outfile.write('\t<attribute name="genomeName" value="' + microarray.genome_name.name + '" />\n')
                outfile.write('\t<attribute name="genomeVersion" value="' + microarray.genome_version + '" />\n')
                exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file