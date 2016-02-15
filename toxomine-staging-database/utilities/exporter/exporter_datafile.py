# Python imports
import commands, os, re, string

# Core Django imports

# Local app imports
from datafiles.models import PersistentDataFile, SubmissionDataFile
from submissions.models import Submission, AppliedProtocol, SubmissionData

import exporter_utility

######################################################################################################
##  Export Persistent DataFile as InterMine Item
######################################################################################################
def export_persistent_datafile_items(file_path, url) :
    persistent_datafiles = PersistentDataFile.objects.all() # get all objects
    
    if persistent_datafiles: # check if empty
        outfile = open(file_path+'/persistent-datafile-items.xml', 'w') # open and write to *-items.xml

        for persistent_datafile in persistent_datafiles:
            submission_data_list = SubmissionData.objects.all().filter(object_id=persistent_datafile.id)
            
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
                outfile.write('<item id="PersistentDataFile_' + str(persistent_datafile.id) + '" class="PersistentDataFile">\n')
                outfile.write('\t<attribute name="name" value="' + persistent_datafile.name + '" />\n')
                outfile.write('\t<attribute name="type" value="' + persistent_datafile.file_type.name + '" />\n')
                outfile.write('\t<attribute name="url" value="' + url + '/persistent/' + persistent_datafile.name + '" />\n')
                exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')

        outfile.close() # close file 

######################################################################################################
##  Export Submission DataFile as InterMine Item
######################################################################################################
def export_submission_datafile_items(file_path, url) :
    
    # create directories if it doesn't exists
    if not os.path.exists(file_path+'/peaks/chromosome'):
        os.makedirs(file_path+'/peaks/chromosome')
    if not os.path.exists(file_path+'/peaks/contig'):
        os.makedirs(file_path+'/peaks/contig')
    if not os.path.exists(file_path+'/peaks/supercontig'):
        os.makedirs(file_path+'/peaks/supercontig')
    if not os.path.exists(file_path+'/gene_list'):
        os.makedirs(file_path+'/gene_list')

    submission_datafiles = SubmissionDataFile.objects.all() # get all objects
    
    gene_list_list = [] # for submission data gene list
    
    if submission_datafiles: # check if empty
        outfile = open(file_path+'/submission-datafile-items.xml', 'w') # open and write to *-items.xml

        for submission_datafile in submission_datafiles:
            submission_data_list = SubmissionData.objects.all().filter(object_id=submission_datafile.id)

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
                outfile.write('<item id="SubmissionDataFile_' + str(submission_datafile.id) + '" class="SubmissionDataFile">\n')
                outfile.write('\t<attribute name="name" value="' + submission_datafile.name + '" />\n')
                outfile.write('\t<attribute name="type" value="' + submission_datafile.file_type.name + '" />\n')

                submission_id_list = submission_datafile.name.split('_')
                outfile.write('\t<attribute name="url" value="' + url + '/' + submission_id_list[0] + '/' + submission_datafile.name + '" />\n')

                exporter_utility.write_collection_items(outfile, submission_list, 'Submission', 'submissions')
                outfile.write('</item>\n')
                
                if 'peaks' in submission_datafile.name:
                    export_peaks_submission_datafile(submission_datafile.data_file.path, file_path+'/peaks/', submission_datafile.name) # export peaks.gff into one folder

                if 'gene_list' in submission_datafile.name:
                    export_gene_list_submission_datafile(submission_datafile.data_file.path, file_path+'/gene_list/'+submission_datafile.name) # export of gene_list.txt
                    gene_list_list.append(file_path+'/gene_list/'+submission_datafile.name) # append to gene list list

        outfile.close() # close file

    if gene_list_list: # consolidate gene list into one list
        consolidate_gene_list_submission_datafile(file_path, gene_list_list)

def export_peaks_submission_datafile(file_path, new_file_path, new_file_name):
    # Read the content of file in
    datafile = open(file_path, 'rU')
    file_content = datafile.readlines()
    datafile.close()

    # Go through each line and figure out if supercontig and contig should also be included
    chromosome = 'n'
    super_contig = 'n'
    contig = 'n'
    for row in range(0,len(file_content)):
        # For ME49 chromosome
        m = re.match(r"TGME49_chr", string.strip(file_content[row]))
        if m :
            chromosome = 'y'
        # For ME49 contig
        n = re.match(r"ABPA", string.strip(file_content[row]))
        if n :
            contig = 'y'
        # For ME49 super contig
        o = re.match(r"tgme49_asmbl", string.strip(file_content[row]))
        if o :
            super_contig = 'y'

    if chromosome == 'y':
        datafile = open(new_file_path + 'chromosome/' + new_file_name, 'w')
        for row in range(0,len(file_content)):
            # For ME49 chromosome
            m = re.match(r"TGME49_chr", string.strip(file_content[row]))
            if m :
                datafile.write(file_content[row])
        datafile.close()

    if contig == 'y':
        datafile = open(new_file_path + 'contig/' + new_file_name, 'w')
        for row in range(0,len(file_content)):
            # For ME49 contig
            n = re.match(r"ABPA", string.strip(file_content[row]))
            if n :
                datafile.write(file_content[row])
        datafile.close()    

    if super_contig == 'y':
        datafile = open(new_file_path + 'supercontig/' + new_file_name, 'w')
        for row in range(0,len(file_content)):
            # For ME49 super contig
            o = re.match(r"tgme49_asmbl", string.strip(file_content[row]))
            if o :
                datafile.write(file_content[row])
        datafile.close()  

def export_gene_list_submission_datafile(file_path, new_file_path):
    # Read the content of file in
    datafile = open(file_path, 'rU')
    file_content = datafile.readlines()
    datafile.close()

    datafile = open(new_file_path, 'w')    
    # Go through each line and modify
    for row in range(0,len(file_content)):
        datafile.write(file_content[row])
    datafile.close()

def consolidate_gene_list_submission_datafile(file_path, gene_list_list):
    cmd  = "rm " + file_path + '/gene_list/gene_list.txt'
    statusCommands = commands.getstatusoutput(cmd)    
    
    out_datafile = open(file_path+'/gene_list/gene_list.txt', 'a')
    
    for gene_list in gene_list_list: 
        # Read the content of file in
        in_datafile = open(gene_list, 'rU')
        file_content = in_datafile.readlines()
        in_datafile.close()

        # Go through each line and modify
        for row in range(0,len(file_content)):
            out_datafile.write(file_content[row])
        
        cmd  = "rm " + gene_list
        statusCommands = commands.getstatusoutput(cmd) 

    out_datafile.close()