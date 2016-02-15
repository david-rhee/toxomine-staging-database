# Python imports
import json, re, urllib2
from datetime import datetime

# Core Django imports
from django.core.exceptions import ValidationError

# Local app imports
from general.models import Db, Dbxref
from publications.models import Author, Publication, PublicationAuthor, PublicationDbxref

######################################################################################################
##  Get or Create Publication
######################################################################################################
def get_publication(unique_name, pmid):
    #check if publication exist, if so return, if not create new
    try:
        result = get_esummary_pmid(pmid)
            
        tmp_date = datetime.strptime(result["result"][pmid]["sortpubdate"], '%Y/%m/%d %H:%M')
        
        publication = Publication(title=result["result"][pmid]["title"],
                                  volume=result["result"][pmid]["volume"],
                                  issue=result["result"][pmid]["issue"],
                                  publication_year=tmp_date.strftime('%Y-%m-%d'),
                                  pages=result["result"][pmid]["pages"],
                                  unique_name=pmid+'-'+result["result"][pmid]["title"],
                                  publisher=result["result"][pmid]["fulljournalname"])
        
        publication.validate_unique()
        publication.save()            

        db = Db.objects.get(name='Pubmed')

        dbxref = Dbxref(accession=pmid, version='1', db=db)
        dbxref.validate_unique()
        dbxref.save()
        
        publication_dbxref = PublicationDbxref(publication=publication, dbxref=dbxref)
        publication_dbxref.validate_unique()
        publication_dbxref.save()

        rank = 1
        tmp_list = result["result"][pmid]["authors"]
        for tmp in tmp_list:
            author = get_author(tmp["name"])
            
            publication_author = PublicationAuthor(rank=rank, publication=publication, author=author)
            publication_author.validate_unique()
            publication_author.save()
            
            rank+=1

    except ValidationError as e:
        publication = Publication.objects.get(unique_name=pmid+'-'+result["result"][pmid]["title"])

    return publication

######################################################################################################
##  Get or Create Author
######################################################################################################
def get_author(name):
    #check if author exist, if so return, if not create new
    try:    
        author = Author(name=name)
        author.validate_unique()
        author.save()
    except ValidationError as e:        
        author = Author.objects.get(name=name)

    return author

######################################################################################################
##  Get Publication information from pubmed
######################################################################################################
def esummary_pmid(pmid):
    try:
        req = urllib2.Request('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&rettype=abstract&id='+pmid)
        returned = urllib2.urlopen(req)
        response = returned.read()
        m = re.search(r"error", response)
        if m:
            return 'none'
        else :
            return json.loads(response)

    except urllib2.URLError as e:
        return 'urlerror'

def get_esummary_pmid(pmid):
    result = esummary_pmid(pmid)
    while result == 'urlerror':
        result = esummary_pmid(pmid)
    return result