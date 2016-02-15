###################################################################
# Python imports

# Core Django imports

# Local app imports
from antibodies.models import Antibody
from genes.models import Gene
from toxoplasmagondiis.models import ToxoplasmaMutant

import exporter_utility

######################################################################################################
##  Export Gene as InterMine Item
######################################################################################################
def export_gene_items(file_path) :
    genes = Gene.objects.all() # get all lab objects

    if genes: # check if empty
        outfile = open(file_path+'/gene-items.xml', 'w') # open and write to lab-items.xml

        for gene in genes:
            toxoplasma_mutant_list = ToxoplasmaMutant.objects.all().filter(target_gene=gene)
            antibody_list = Antibody.objects.all().filter(target_gene=gene)

            # Only export if there is a related toxoplasma mutant or antibody
            if toxoplasma_mutant_list or antibody_list: 
                outfile.write('<item id="Gene_' + str(gene.id) + '" class="Gene">\n')
                outfile.write('\t<attribute name="primaryIdentifier" value="' + str(gene.gene_id) + '" />\n')
                outfile.write('\t<attribute name="symbol" value="' + str(gene.gene_id) + '" />\n')
                outfile.write('\t<attribute name="name" value="' + str(gene.description) + '" />\n')
                
                if toxoplasma_mutant_list:
                    exporter_utility.write_collection_items(outfile, toxoplasma_mutant_list, 'ToxoplasmaMutant', 'toxoplasmaMutants')
                if antibody_list:
                    exporter_utility.write_collection_items(outfile, antibody_list, 'Antibody', 'antibodies')

                outfile.write('</item>\n')
        
        outfile.close() # close file