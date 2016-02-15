# Python imports
import csv, os, re, string, sys
from datetime import datetime, timedelta

# Setup environ
import django
sys.path.append('../..')
os.environ['DJANGO_SETTINGS_MODULE'] = "toxomine-staging-database.settings.local"

# Local app imports
import importer_antibody
import importer_data_analysis
import importer_datafile
import importer_experiment
import importer_experimental_factor
import importer_gene
import importer_microarray
import importer_ontology
import importer_organism
import importer_project
import importer_protocol
import importer_publication
import importer_submission
import importer_toxoplasma_mutant
import importer_user

# Setup django
django.setup()

######################################################################################################
##  Object Loaders
######################################################################################################
def load_antibody(raw_data, row):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    antibody_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            target_name = raw_data[row][1]
            target_name = target_name[1:-1]
            tagged = raw_data[row][2]
            tagged = tagged[1:-1]
            tag_target = raw_data[row][3]
            tag_target = tag_target[1:-1]
            source = raw_data[row][4]
            source = source[1:-1]
            catalog_number = raw_data[row][5]
            catalog_number = catalog_number[1:-1]
            epitope = raw_data[row][6]
            epitope = epitope[1:-1]
            lot_number = raw_data[row][7]
            lot_number = lot_number[1:-1]
            ifa_localization = raw_data[row][8]
            ifa_localization = ifa_localization[1:-1]
            chip_peaks = raw_data[row][9]
            chip_peaks = chip_peaks[1:-1]
            monoclonal = raw_data[row][10]
            monoclonal = monoclonal[1:-1]
            isotype = raw_data[row][11]
            isotype = isotype[1:-1]
            immunogen_source = raw_data[row][12]
            immunogen_source = immunogen_source[1:-1]
            conjugation = raw_data[row][13]
            conjugation = conjugation[1:-1]
            validated = raw_data[row][14]
            validated = validated[1:-1]
            url = raw_data[row][15]
            url = url[1:-1]
            animal_host = raw_data[row][16]
            animal_host = animal_host[1:-1]
            target_gene = raw_data[row][17]
            target_gene = target_gene[1:-1]

            #load ontology term
            animal_host = importer_ontology.get_ontology_term("antibody", "antibody host organism", animal_host) # get ontology term

            #load of Genes
            if target_gene:
                target_gene = importer_gene.get_gene(target_gene)

            if name and target_name and target_gene:
                antibody = importer_antibody.get_antibody_with_target_gene(name, target_name, tagged, tag_target, source, catalog_number, epitope, lot_number, ifa_localization,
                                                                                             chip_peaks, monoclonal, isotype, immunogen_source, conjugation, validated, url, animal_host, target_gene) # return antibody
                antibody_list.append(antibody)
            elif name and target_name:
                antibody = importer_antibody.get_antibody_without_target_gene(name, target_name, tagged, tag_target, source, catalog_number, epitope, lot_number, ifa_localization,
                                                                                                chip_peaks, monoclonal, isotype, immunogen_source, conjugation, validated, url, animal_host) # return antibody
                antibody_list.append(antibody)

    return antibody_list

def load_data_analysis(raw_data, row):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    data_analysis_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            version = raw_data[row][1]
            version = version[1:-1]
            module = raw_data[row][2]
            module = module[1:-1]
            platform = raw_data[row][3]
            platform = platform[1:-1]
            data_analysis_type = raw_data[row][4]
            data_analysis_type = data_analysis_type[1:-1]
            parameter = raw_data[row][5]
            parameter = parameter[1:-1]
            notes = raw_data[row][6]
            notes = notes[1:-1]
            
            #load ontology term
            data_analysis_type = importer_ontology.get_ontology_term("data analysis", "data analysis type", data_analysis_type) # get ontology term

            if name and version and module and parameter:
                data_analysis = importer_data_analysis.get_data_analysis(name, version, module, platform, data_analysis_type, parameter, notes) # return data analysis
                data_analysis_list.append(data_analysis)

    return data_analysis_list

def load_experiment(raw_data, row, user, project, publication_list):
    #move down to name
    row+=1
    name = raw_data[row][1]
    if name.startswith('"') and name.endswith('"'):
        name = name[1:-1]

        #move down to description
        row+=1
        description = raw_data[row][1]
        if description.startswith('"') and description.endswith('"'):
            description = description[1:-1]

            #move down to category
            row+=1
            category = raw_data[row][1]
            if category.startswith('"') and category.endswith('"'):
                category = category[1:-1]
                category = importer_ontology.get_ontology_term("experiment", "experiment category", category) # get ontology term

                #move down to publishable
                row+=1
                publishable = raw_data[row][1]
                if publishable.startswith('"') and publishable.endswith('"'):
                    publishable = publishable[1:-1]
                    if publishable == 'True':
                        publishable = True
                    else:
                        publishable = False

                if name and description and category:
                    return importer_experiment.get_experiment(name, description, category, publishable, user, project, publication_list) # return experiment

    sys.exit('Check experiment information')

def load_experimental_factor(raw_data, row):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    experimental_factor_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            value = raw_data[row][1]
            value = value[1:-1]

            #load ontology term
            name = importer_ontology.get_ontology_term("experimental factor", "experimental factor type", name) # get ontology term

            if name and value:
                experimental_factor = importer_experimental_factor.get_experimental_factor(name, value) # return experimental factor
                experimental_factor_list.append(experimental_factor)

    return experimental_factor_list

def load_microarray(raw_data, row):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    microarray_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            platform = raw_data[row][1]
            platform = platform[1:-1]
            microarray_format = raw_data[row][2]
            microarray_format = microarray_format[1:-1]
            version = raw_data[row][3]
            version = version[1:-1]
            genome_name = raw_data[row][4]
            genome_name = genome_name[1:-1]
            genome_version = raw_data[row][5]
            genome_version = genome_version[1:-1]

            #load ontology term
            platform = importer_ontology.get_ontology_term("microarray", "microarray platform", platform) # get ontology term
            microarray_format = importer_ontology.get_ontology_term("microarray", "microarray format", microarray_format) # get ontology term
            genome_name = importer_ontology.get_ontology_term("microarray", "microarray genome name", genome_name) # get ontology term

            if name and platform and microarray_format and genome_name and genome_version:
                microarray = importer_microarray.get_microarray(name, platform, microarray_format, version, genome_name, genome_version) # return microarray
                microarray_list.append(microarray)

    return microarray_list

def load_persistent_data_file(raw_data, row, file_path):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    persistent_datafile_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            datafile_type = raw_data[row][1]
            datafile_type = datafile_type[1:-1]

            #load ontology term
            datafile_type = importer_ontology.get_ontology_term("datafile", "datafile type", datafile_type) # get ontology term

            if name and datafile_type:
                persistent_datafile = importer_datafile.get_persistent_datafile(name, datafile_type, file_path+'/R11')
                persistent_datafile_list.append(persistent_datafile)
   
    return persistent_datafile_list

def load_project(raw_data, row, user, publication_list):
    #move down to name
    row+=1
    name = raw_data[row][1]
    if name.startswith('"') and name.endswith('"'):
        name = name[1:-1]

        #move down to description
        row+=1
        description = raw_data[row][1]
        if description.startswith('"') and description.endswith('"'):
            description = description[1:-1]

            #move down to experimental approaches
            row+=1
            experimental_approaches = raw_data[row][1]
            if experimental_approaches.startswith('"') and experimental_approaches.endswith('"'):
                experimental_approaches = experimental_approaches[1:-1]

                #move down to data generation
                row+=1
                data_generation = raw_data[row][1]
                if data_generation.startswith('"') and data_generation.endswith('"'):
                    data_generation = data_generation[1:-1]

                    #move down to publishable
                    row+=1
                    publishable = raw_data[row][1]
                    if publishable.startswith('"') and publishable.endswith('"'):
                        publishable = publishable[1:-1]
                        if publishable == 'True':
                            publishable = True
                        else:
                            publishable = False
                        
                        if name and description and experimental_approaches and data_generation:
                            return importer_project.get_project(name, description, experimental_approaches, data_generation, publishable, user, publication_list) # return project

    sys.exit('Check project information')

def load_protocol(raw_data, row, submission, toxoplasma_mutant_list, antibody_list, experimental_factor_list, microarray_list, #sequencing_list,
                  data_analysis_list, persistent_datafile_list, submission_datafile_list):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    protocol_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            description = raw_data[row][1]
            description = description[1:-1]
            protocol_type = raw_data[row][2]
            protocol_type = protocol_type[1:-1]
            inside_attribute_count = int(raw_data[row][3])

            #load ontology term
            protocol_type = importer_ontology.get_ontology_term("protocol", "protocol type", protocol_type) # get ontology term

            if name and description and protocol_type and (inside_attribute_count >= 0):
                protocol = importer_protocol.get_protocol(name, description, protocol_type) # return protocol
                protocol_list.append(protocol)
                
                #create applied protocol and link
                if (i == 0) :
                    applied_protocol = importer_submission.get_applied_protocol_start_node((i+1), protocol, submission)
                    previous_applied_protocol = applied_protocol
                else :
                    applied_protocol = importer_submission.get_applied_protocol_other_node((i+1), protocol, submission, previous_applied_protocol)
                    previous_applied_protocol = applied_protocol
                    
                for x in range(0, inside_attribute_count):
                    #move right for data
                    tmp_holder = raw_data[row][x+4]
                    tmp_holder = tmp_holder[1:-1]
                    #check the data type for toxoplasmaMutant
                    s = re.search(r"^toxoplasmaMutant", tmp_holder)
                    if s:
                        importer_submission.get_toxoplasma_mutant_submission_data(tmp_holder, toxoplasma_mutant_list, applied_protocol, "toxoplasmaMutant")
                    #check the data type for antibody
                    s = re.search(r"^antibody", tmp_holder)
                    if s:
                        importer_submission.get_antibody_submission_data(tmp_holder, antibody_list, applied_protocol, "antibody")
                    #check the data type for experimentalFactor
                    s = re.search(r"^experimentalFactor", tmp_holder)
                    if s:
                        importer_submission.get_experimental_factor_submission_data(tmp_holder, experimental_factor_list, applied_protocol, "experimentalFactor")
                    #check the data type for microarray
                    s = re.search(r"^microarray", tmp_holder)
                    if s:
                        importer_submission.get_microarray_submission_data(tmp_holder, microarray_list, applied_protocol, "microarray")
                    #check the data type for dataAnalysis
                    s = re.search(r"^dataAnalysis", tmp_holder)
                    if s:
                        importer_submission.get_data_analysis_submission_data(tmp_holder, data_analysis_list, applied_protocol, "dataAnalysis")
                    #check the data type for persistentDataFile
                    s = re.search(r"^persistentDataFile", tmp_holder)
                    if s:
                        importer_submission.get_persistent_datafile_submission_data(tmp_holder, persistent_datafile_list, applied_protocol, "persistentDataFile")
                    #check the data type for submissionDataFile
                    s = re.search(r"^submissionDataFile", tmp_holder)
                    if s:
                        importer_submission.get_submission_datafile_submission_data(tmp_holder, submission_datafile_list, applied_protocol, "submissionDataFile")

    return protocol_list

def load_publication(raw_data, row):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    publication_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            pmid = raw_data[row][0]
            pmid = pmid[1:-1]
            unique_name = raw_data[row][1]
            unique_name = unique_name[1:-1]

            if unique_name and pmid:
                publication = importer_publication.get_publication(unique_name, pmid) # return experimental factor
                publication_list.append(publication)

    return publication_list

def load_submission(raw_data, row, user, experiment, publication_list):
    #move down to given_name
    row+=1
    given_name = raw_data[row][1]
    if given_name.startswith('"') and given_name.endswith('"'):
        given_name = given_name[1:-1]

        #move down to description
        row+=1
        description = raw_data[row][1]
        if description.startswith('"') and description.endswith('"'):
            description = description[1:-1]

            #move down to technique
            row+=1
            technique = raw_data[row][1]
            if technique.startswith('"') and technique.endswith('"'):
                technique = technique[1:-1]
                technique = importer_ontology.get_ontology_term("submission", "submission technique", technique) # get ontology term

                #move down to quality_control
                row+=1
                quality_control = raw_data[row][1]
                if quality_control.startswith('"') and quality_control.endswith('"'):
                    quality_control = quality_control[1:-1]
                    quality_control = importer_ontology.get_ontology_term("submission", "submission quality control", quality_control) # get ontology term
                
                    #move down to replicate series
                    row+=1
                    replicate_series = raw_data[row][1]
                    if replicate_series.startswith('"') and replicate_series.endswith('"'):
                        replicate_series = replicate_series[1:-1]

                        #move down to replicate
                        row+=1
                        date_replicate = raw_data[row][1]
                        if date_replicate.startswith('"') and date_replicate.endswith('"'):
                            date_replicate = date_replicate[1:-1]

                            #move down to note
                            row+=1
                            notes = raw_data[row][1]
                            if notes.startswith('"') and notes.endswith('"'):
                                notes = notes[1:-1]

                            #move down to publishable
                            row+=1
                            publishable = raw_data[row][1]
                            if publishable.startswith('"') and publishable.endswith('"'):
                                publishable = publishable[1:-1]
                                if publishable == 'True':
                                    publishable = True
                                else:
                                    publishable = False
                    
                                if given_name and description and technique and quality_control and replicate_series and date_replicate and notes:
                                    return importer_submission.get_submission(given_name, description, technique, quality_control,
                                                                                                replicate_series, date_replicate, notes, publishable, user, experiment, publication_list) # return submission

    sys.exit('Check submission information')

def load_submission_data_file(raw_data, row, file_path, submission_name, antibody_list):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    submission_datafile_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            datafile_type = raw_data[row][1]
            datafile_type = datafile_type[1:-1]
            rep_name = raw_data[row][2]
            rep_name = rep_name[1:-1]
            publishable = raw_data[row][3]
            publishable = publishable[1:-1]
            if publishable == 'True':
                publishable = True
            else:
                publishable = False

            #load ontology term
            datafile_type = importer_ontology.get_ontology_term("datafile", "datafile type", datafile_type) # get ontology term

            if name and datafile_type:
                submission_datafile = importer_datafile.get_submission_datafile(name, datafile_type, file_path+'/'+rep_name, publishable, submission_name, antibody_list)
                submission_datafile_list.append(submission_datafile)
   
    return submission_datafile_list

def load_toxoplasma_mutant(raw_data, row):
    #move down to attribute count
    row+=1
    attribute_count = int(raw_data[row][1])

    toxoplasma_mutant_list = []

    if attribute_count > 0:
        row+=1
        for i in range(0, attribute_count):
            #move down to data
            row+=1
            name = raw_data[row][0]
            name = name[1:-1]
            target_name = raw_data[row][1]
            target_name = target_name[1:-1]
            background = raw_data[row][2]
            background = background[1:-1]
            selection = raw_data[row][3]
            selection = selection[1:-1]
            mutation_type = raw_data[row][4]
            mutation_type = mutation_type[1:-1]
            promoter = raw_data[row][5]
            promoter = promoter[1:-1]
            organism = raw_data[row][6]
            organism = organism[1:-1]
            target_gene = raw_data[row][7]
            target_gene = target_gene[1:-1]

            #load organism
            organism = importer_organism.get_organism(organism)

            #load ontology term
            background = importer_ontology.get_ontology_term("toxoplasma mutant", "toxoplasma mutant background", background) # get ontology term
            selection = importer_ontology.get_ontology_term("toxoplasma mutant", "toxoplasma mutant selection", selection) # get ontology term
            mutation_type = importer_ontology.get_ontology_term("toxoplasma mutant", "toxoplasma mutant mutation type", mutation_type) # get ontology term
            promoter = importer_ontology.get_ontology_term("toxoplasma mutant", "toxoplasma mutant promoter", promoter) # get ontology term

            #load of Genes
            if target_gene:
                target_gene = importer_gene.get_gene(target_gene)

            if name and target_name and background and selection and mutation_type and promoter and organism and target_gene:
                toxoplasma_mutant = importer_toxoplasma_mutant.get_toxoplasma_mutant_with_target_gene(name, target_name, background, selection,
                                                                     mutation_type, promoter, organism, target_gene) # return toxoplasma mutant
                toxoplasma_mutant_list.append(toxoplasma_mutant)

            elif name and target_name and background and selection and mutation_type and promoter and organism:
                toxoplasma_mutant = importer_toxoplasma_mutant.get_toxoplasma_mutant_without_target_gene(name, target_name, background, selection,
                                                                     mutation_type, promoter, organism) # return toxoplasma mutant
                toxoplasma_mutant_list.append(toxoplasma_mutant)

    return toxoplasma_mutant_list

def load_user(raw_data, row):
    #move down to name
    row+=1
    username = raw_data[row][1]
    if username.startswith('"') and username.endswith('"'):
        username = username[1:-1]
        if username:
            return importer_user.get_user(username) # return user
    
    sys.exit('Check user name')

######################################################################################################
##  Data Loader
######################################################################################################
def load_data(file_path, data_file):
    with open(data_file, 'rb') as f:
        raw_data = [row for row in csv.reader(f.read().splitlines())]
        
        user_list = []
        
        for row in range(0, len(raw_data)):
            tmp_list = raw_data[row]
    
            #read user info
            if tmp_list[0] == 'user':
                user = load_user(raw_data, row)
                user_list.append(user)

            #read publication info
            if tmp_list[0] == 'publication':
                publication_list = load_publication(raw_data, row)

            #read project info
            if tmp_list[0] == 'project':
                project = load_project(raw_data, row, user_list[0], publication_list)
                for index, user_from_list in enumerate(user_list):
                    if index != 0 :
                        importer_project.add_project_contributor(project, user_from_list)
            #read experiment info
            if tmp_list[0] == 'experiment':
                experiment = load_experiment(raw_data, row, user_list[0], project, publication_list)
                for index, user_from_list in enumerate(user_list):
                    if index != 0 :
                        importer_experiment.add_experiment_contributor(experiment, user_from_list)
            #read submission info
            if tmp_list[0] == 'submission':
                submission = load_submission(raw_data, row, user_list[0], experiment, publication_list)
                for index, user_from_list in enumerate(user_list):
                    if index != 0 :
                        importer_submission.add_submission_contributor(submission, user_from_list)

            #read toxoplasmaMutant info
            if tmp_list[0] == 'toxoplasmaMutant':
                toxoplasma_mutant_list = load_toxoplasma_mutant(raw_data, row)
            #read antibody info
            if tmp_list[0] == 'antibody':
                antibody_list = load_antibody(raw_data, row)
            #read experimentalFactor info
            if tmp_list[0] == 'experimentalFactor':
                experimental_factor_list = load_experimental_factor(raw_data, row)
            #read microarray info
            if tmp_list[0] == 'microarray':
                microarray_list = load_microarray(raw_data, row)
            ##read sequencing info
            #if tmp_list[0] == 'sequencing':
            #    sequencing_list = load_sequencing(raw_data, row)
            #read dataAnalysis info
            if tmp_list[0] == 'dataAnalysis':
                data_analysis_list = load_data_analysis(raw_data, row)
            #read persistentDataFile info
            if tmp_list[0] == 'persistentDataFile':
                persistent_datafile_list = load_persistent_data_file(raw_data, row, file_path)
            #read submissionDataFile info
            if tmp_list[0] == 'submissionDataFile':
                submission_datafile_list = load_submission_data_file(raw_data, row, file_path, submission.generated_id, antibody_list)
            #read protocol info
            if tmp_list[0] == 'protocol':
                protocol_list = load_protocol(raw_data, row, submission, toxoplasma_mutant_list, antibody_list, experimental_factor_list, microarray_list, #sequencing_list,
                                              data_analysis_list, persistent_datafile_list, submission_datafile_list)

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
            file_list = string.split(string.strip(raw[1]))

            for csv_file in file_list:
                load_data(file_path, file_path + csv_file)

        except OSError:
            sys.exit('Check arguments - config file not found')

    else:
        sys.exit('Check arguments - importer_config_file.txt')

if __name__=="__main__":
    main()
