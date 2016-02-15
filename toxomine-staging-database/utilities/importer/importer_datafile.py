# Python imports
import re, string
from datetime import datetime

# Core Django imports
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import locks, File
from django.core.files.storage import FileSystemStorage, Storage

# Local app imports
from datafiles.models import PersistentDataFile, SubmissionDataFile

######################################################################################################
##  Get or Create Persistent DataFile
######################################################################################################
def get_persistent_datafile(name, file_type, file_path):        
    #check if persistent_datafile exists, if so return, if not create new
    try:
        datafile = open(file_path + '/' + name, 'ro') # open given file

        persistent_datafile = PersistentDataFile(name=name, given_name=name,
                                                  data_generation=datetime.now(), publishable=True,
                                                  file_type=file_type,
                                                  date_created=datetime.now(), date_modified=datetime.now())
        persistent_datafile.validate_unique()
        persistent_datafile.save()

        persistent_datafile.data_file.storage.save('persistent/'+name, datafile) # save to persistent/ directory
        persistent_datafile.data_file = 'persistent/' + name # save data_file
        persistent_datafile.save()

        datafile.close()
    
    except ValidationError as e:
        persistent_datafile = PersistentDataFile.objects.get(name=name)
    
    return persistent_datafile

######################################################################################################
##  Get or Create Submission DataFile
######################################################################################################
def get_submission_datafile(name, file_type, file_path, publishable, submission_name, antibody_list):        
    #check if submission_datafile exists, if so return, if not create new
    try:
        new_name = submission_name + '_' + name
        datafile = open(file_path + '/' + name, 'r') # open given file

        submission_datafile = SubmissionDataFile(name=new_name, given_name=name,
                                                  data_generation=datetime.now(), publishable=publishable,
                                                  file_type=file_type,
                                                  date_created=datetime.now(), date_modified=datetime.now())
        submission_datafile.validate_unique()
        submission_datafile.save()

        new_path = submission_datafile.data_file.storage.save(submission_name+'/'+new_name, datafile) # save to generated_id/ directory
        submission_datafile.data_file = submission_name+'/' + new_name # save data_file
        submission_datafile.save()

        datafile.close()
        
        if 'peaks' in name:
            modify_peaks_submission_datafile(settings.MEDIA_ROOT+'/'+new_path, submission_name, antibody_list) # modify the content of peaks.gff
        
        if 'gene_list' in name:
            modify_gene_list_submission_datafile(settings.MEDIA_ROOT+'/'+new_path, submission_name) # modify the content of gene_list.txt

    except ValidationError as e:
        submission_datafile = SubmissionDataFile.objects.get(given_name=name)
    
    return submission_datafile

######################################################################################################
##  Modify peaks file so that it contains the submission information
######################################################################################################
def modify_peaks_submission_datafile(file_path, submission_name, antibody_list):
    # Read the content of file in
    datafile = open(file_path, 'rU')
    file_content = datafile.readlines()
    datafile.close()

    datafile = open(file_path, 'w')    
    # Go through each line and modify
    for row in range(0,len(file_content)):
        if row == 0 :
            datafile.write(file_content[row]) # skip line 1
        else:
            datafile.write(string.split(string.strip(file_content[row]))[0])
            datafile.write('\t')
            datafile.write(string.split(string.strip(file_content[row]))[1])
            datafile.write('\t')
            datafile.write('histone_binding_site')
            datafile.write('\t')
            datafile.write(string.split(string.strip(file_content[row]))[3])
            datafile.write('\t')
            datafile.write(string.split(string.strip(file_content[row]))[4])
            datafile.write('\t')
            datafile.write(string.split(string.strip(file_content[row]))[5])
            datafile.write('\t')
            datafile.write(string.split(string.strip(file_content[row]))[6])
            datafile.write('\t')
            datafile.write(string.split(string.strip(file_content[row]))[7])
            datafile.write('\t')            
            
            tmpString = string.split(string.strip(file_content[row]))[8]
            if tmpString.count(';') == 3:
                one,two,three,four = tmpString.split(';')
                m = re.match(r"(fdr=)(\S*)(orig_probe_location)(\S*)", three)
                if m:
                    fdr = m.group(2)
                else:
                    fdr = -1
            elif tmpString.count(';') == 5:
                one,two,three,four,five,six = tmpString.split(';')
                m = re.match(r"(fdr=)(\S*)(probe_id)(\S*)", three)
                if m:
                    fdr = m.group(2)
                else:
                    fdr = -1

            antibody_name = ''
            if len(antibody_list) > 1 :
                for antibody in antibody_list:
                    antibody_name = antibody_name + '_' + antibody.target_name
            else:
                antibody = antibody_list[0]
                antibody_name = antibody.target_name
            
            datafile.write('ID=' + antibody_name + '_' + string.split(string.strip(file_content[row]))[0] + '_' + string.split(string.strip(file_content[row]))[3] + '_' +
                           string.split(string.strip(file_content[row]))[3] + '_' + submission_name + ';Submission=' + submission_name + ';fdr=' + fdr)
            datafile.write('\n') 
    datafile.close()

######################################################################################################
##  Modify gene list so that it contains the submission information
######################################################################################################
def modify_gene_list_submission_datafile(file_path, submission_name):
    # Read the content of file in
    datafile = open(file_path, 'rU')
    file_content = datafile.readlines()
    datafile.close()
    
    datafile = open(file_path, 'w')    
    # Go through each line and modify
    for row in range(0,len(file_content)):
        datafile.write(string.split(string.strip(file_content[row]))[0])
        datafile.write('\t')
        datafile.write(string.split(string.strip(file_content[row]))[1])
        datafile.write('\t')            
        datafile.write(submission_name + '_gene_list')
        datafile.write('\t')            
        datafile.write(submission_name)
        datafile.write('\n') 
    datafile.close()