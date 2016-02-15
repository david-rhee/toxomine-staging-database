# Python imports

# Core Django imports

# Local app imports
from protocols.models import Protocol
from submissions.models import AppliedProtocol

import exporter_utility

######################################################################################################
##  Export Protocol as InterMine Item
######################################################################################################
def export_protocol_items(file_path) :
    protocols = Protocol.objects.all().filter(current=True) # get all objects
    
    if protocols: # check if empty
        outfile = open(file_path+'/protocol-items.xml', 'w') # open and write to *-items.xml

        for protocol in protocols:
            submission_list = [] # submissions
            applied_protocol_list = AppliedProtocol.objects.all().filter(protocol=protocol)
            for applied_protocol in applied_protocol_list:
                if applied_protocol.submission.publishable == True:
                    submission_list.append(applied_protocol.submission)
            submission_list = list(set(submission_list)) # Get rid of duplicates

            # Only export if there is a related objects
            if submission_list:
                outfile.write('<item id="Protocol_' + str(protocol.id) + '" class="Protocol">\n')
                outfile.write('\t<attribute name="name" value="' + protocol.name + '" />\n')
                outfile.write('\t<attribute name="description" value="' + protocol.description + '" />\n')
                outfile.write('\t<attribute name="type" value="' + protocol.protocol_type.name + '" />\n')
                outfile.write('\t<attribute name="version" value="' + str(protocol.version) + '" />\n')
                exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file