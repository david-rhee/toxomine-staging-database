######################################################################################################
##  Export Utilities - Write collection items of objects
###################################################################################################### 
def write_collection_items(outfile, item_objects, item_object_name, collection_name) :
    outfile.write('\t<collection name="'+ collection_name +'">')
    for item_object in item_objects:
        outfile.write('<reference ref_id="' + item_object_name + '_' + str(item_object.id) + '"/>')   
    outfile.write('</collection>\n')

######################################################################################################
##  Export Utilities - Write reference item of object
######################################################################################################
def write_reference_item(outfile, item_object, item_object_name, reference_name) :
    outfile.write('\t<reference name="'+ reference_name +'" ref_id="' + item_object_name + '_' + str(item_object.id) + '"/>\n')