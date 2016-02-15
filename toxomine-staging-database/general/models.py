# Core Django imports
from django.db import models

# Third-party app imports

# Local app imports

#####################################################################################################
#  Based on Chado's general module
#####################################################################################################
"""
 The db table contains one row per database authority, that is, one row per curator/creator of bioinformatic data collections.
 Typical databases in bioinformatics are FlyBase, GO, UniProt, NCBI, MGI, etc.
 The authority is generally known by this shortened form, which is unique within the bioinformatics and biomedical realm.
"""
class Db(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    urlprefix = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=255, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"""{name}""".format(
            name=self.name,
        )

"""
 The dbxref table contains one row per version per collection of bioinformatic data, one row per Chado "database".
 The table provides a unique, global, public, stable identifier that can be used to reference a database version.
 Not necessarily an external reference - can reference data items inside the particular chado instance being used.
 Typically a row in a table can be uniquely identified with a primary identifier (called dbxref_id); a table may also
 have secondary identifiers (in a linking table <T>_dbxref). A dbxref is generally written as <DB>:<ACCESSION> or as <DB>:<ACCESSION>:<VERSION>.
"""
class Dbxref(models.Model):
    accession = models.CharField(max_length=255, null=False, blank=False)
    version = models.CharField(max_length=255, default='', blank=True)
    description = models.TextField(blank=True)
    #Relationships    
    db = models.ForeignKey(Db, related_name="%(app_label)s_%(class)s_db")

    class Meta:
        unique_together = ('accession', 'version', 'db')
        ordering = ['db', 'accession']

    def __unicode__(self):
        return u"""{db}:{accession}""".format(
            accession=self.accession,
            db=self.db,
        )