# Python imports

# Core Django imports

# Local app imports
from dataanalyses.models import DataAnalysis
from submissions.models import Submission, AppliedProtocol, SubmissionData

import exporter_utility

######################################################################################################
##  Export DataAnalysis as InterMine Item
######################################################################################################
def export_data_analysis_items(file_path) :
    data_analyses = DataAnalysis.objects.all() # get all objects
    
    if data_analyses: # check if empty
        outfile = open(file_path+'/data-analysis-items.xml', 'w') # open and write to *-items.xml

        for data_analysis in data_analyses:
            submission_data_list = SubmissionData.objects.all().filter(object_id=data_analysis.id)

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
            if submission_data_list or submission_list: 
                outfile.write('<item id="DataAnalysis_' + str(data_analysis.id) + '" class="DataAnalysis">\n')
                outfile.write('\t<attribute name="name" value="' + data_analysis.name + '" />\n')
                outfile.write('\t<attribute name="platform" value="' + data_analysis.platform + '" />\n')
                outfile.write('\t<attribute name="version" value="' + data_analysis.version + '" />\n')
                outfile.write('\t<attribute name="module" value="' + data_analysis.module + '" />\n')
                outfile.write('\t<attribute name="parameter" value="' + data_analysis.parameter + '" />\n')
                if data_analysis.data_analysis_type:
                    outfile.write('\t<attribute name="type" value="' + data_analysis.data_analysis_type.name + '" />\n')
                exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file