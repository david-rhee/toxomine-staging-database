# Python imports

# Core Django imports

# Local app imports
from organisms.models import Organism
from toxoplasmagondiis.models import ToxoplasmaMutant

import exporter_utility

######################################################################################################
##  Export Organism as InterMine Item
######################################################################################################
def export_organism_items(file_path) :
    organisms = Organism.objects.all() # get all lab objects

    if organisms: # check if empty
        outfile = open(file_path+'/organism-items.xml', 'w') # open and write to lab-items.xml

        for organism in organisms:
            toxoplasma_mutant_list = ToxoplasmaMutant.objects.all().filter(organism=organism)

            # Only export if there is a related toxoplasma mutant
            if toxoplasma_mutant_list: 
                outfile.write('<item id="Organism_' + str(organism.id) + '" class="Organism">\n')
                outfile.write('\t<attribute name="taxonId" value="' + str(organism.taxon_id) + '" />\n')
                exporter_utility.write_collection_items(outfile, toxoplasma_mutant_list, 'ToxoplasmaMutant', 'toxoplasmaMutants')
                outfile.write('</item>\n')
        
        outfile.close() # close file