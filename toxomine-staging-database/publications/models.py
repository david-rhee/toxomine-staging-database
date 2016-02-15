# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports
from general.models import Dbxref

#####################################################################################################
#  Based on Chado's publication module
#####################################################################################################
"""
An author for a publication. Note the denormalisation (hence lack of _ in table name) - this is deliberate as it is in general too hard to assign IDs to authors.
"""
class Author(models.Model):
   name = models.CharField(max_length=100, blank=False, unique=True)
   suffix = models.CharField(max_length=100, blank=True)

   def __unicode__(self):
       return u"""{name}""".format(
           name=self.name,
       )

"""
 A documented provenance artefact - publications, documents, personal communication.
"""
class Publication(models.Model):
    title = models.TextField(blank=True)
    volume = models.CharField(max_length=255, blank=True)
    issue = models.CharField(max_length=255, blank=True)
    publication_year = models.DateField(max_length=255, blank=True)
    pages = models.CharField(max_length=255, blank=True)
    unique_name = models.TextField(unique=True, blank=True)
    obsolete = models.BooleanField(default=False)
    publisher = models.CharField(max_length=255, blank=True) 
    #Relationships
    authors = models.ManyToManyField(Author, blank=True, through='PublicationAuthor', related_name="%(app_label)s_%(class)s_authors")
    dbxrefs = models.ManyToManyField(Dbxref, blank=True, through='PublicationDbxref', related_name="%(app_label)s_%(class)s_dbxrefs")

    def __unicode__(self):
        return u"""{title}""".format(
            title=self.title,
        )

"""
Publication to Author M2M relationship
"""
class PublicationAuthor(models.Model):
   rank = models.IntegerField(null=False)
   editor = models.BooleanField(default=False)
   publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_publication")
   author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_author")

   def __unicode__(self):
       return u"""{publication};{author}""".format(
           publication=self.publication,
           author=self.author,
       )

"""
 Publication to Dbxref M2M relationship
"""
class PublicationDbxref(models.Model):
    is_current = models.BooleanField(default=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_publication")
    dbxref = models.ForeignKey(Dbxref, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_dbxref")
    
    def __unicode__(self):
        return u"""{publication};{dbxref}""".format(
           publication=self.publication,
           dbxref=self.dbxref,
        )