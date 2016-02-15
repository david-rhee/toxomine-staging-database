# Python
import os.path
from datetime import datetime, timedelta

# Core Django imports
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm

#####################################################################################################
#  Submission Properties
#  ---------------------
#  Data Files
######################################################################################################
"""
   Function to create unique folder for file upload
"""
def upload_path_handler(instance, filename):
    return os.path.join("user_%d")

"""
Base Class to hold Data File information
"""
class DataFile(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True) # Add Submission ID before given name by user: ex - TC1_GCN5B_DR_R11...
    given_name = models.CharField(max_length=200, null=True, blank=True) # Given name by user
    data_generation = models.DateField(null=True, blank=True)
    publishable = models.BooleanField(default=False, blank=True)
    file_type = models.ForeignKey(OntologyTerm, null=True, related_name="%(app_label)s_%(class)s_file_type")
    data_file = models.FileField(upload_to='.')
    date_created = models.DateField(null=True, blank=True)
    date_modified = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)

    def create_date(self):
        self.date_created = datetime.now()
        self.date_modified = datetime.now()

#####################################################################################################
#  PersistentDataFile
"""
Class to hold Persistent Data File information
"""
class PersistentDataFileManager(models.Manager):
    def get_queryset_publishable(self):
        return super(PersistentDataFileManager, self).get_queryset().filter(publishable=True).order_by('name')

class PersistentDataFile(DataFile):
    # Managers
    objects = models.Manager() # The default manager.
    persistent_datafile_objects = PersistentDataFileManager() # The PersistentDataFile-specific manager.

    def get_data_file(instance, data_file):
        instance.data_file = data_file
        return os.path.join('persistent/', data_file)

    def save(self, *args, **kwargs):
        try:
            this = PersistentDataFile.objects.get(id=self.id)
            if this.data_file:
                if this.data_file != self.data_file:
                    if os.path.isfile(this.data_file.path):
                        this.data_file.delete()
        except:
            pass
        super(PersistentDataFile, self).save(*args, **kwargs)

# Auto-delete files from filesystem when they are unneeded:
@receiver(post_delete, sender=PersistentDataFile)
def auto_delete_persistent_datafile_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.data_file:
        if os.path.isfile(instance.data_file.path):
            instance.data_file.delete(False)

#####################################################################################################
#  SubmissionDataFile
"""
Class to hold Submission Data File information
"""
class SubmissionDataFileManager(models.Manager):
    def get_queryset_publishable(self):
        return super(SubmissionDataFileManager, self).get_queryset().filter(publishable=True).order_by('name')

class SubmissionDataFile(DataFile):
    # Managers
    objects = models.Manager() # The default manager.
    submission_datafile_objects = SubmissionDataFileManager() # The SubmissionDataFile-specific manager.

    def save(self, *args, **kwargs):
        try:
            this = SubmissionDataFile.objects.get(id=self.id)
            if this.data_file:
                if this.data_file != self.data_file:
                    if os.path.isfile(this.data_file.path):
                        this.data_file.delete()
        except:
            pass
        super(SubmissionDataFile, self).save(*args, **kwargs)

# Auto-delete files from filesystem when they are unneeded:
@receiver(post_delete, sender=SubmissionDataFile)
def auto_delete_submission_datafile_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.data_file:
        if os.path.isfile(instance.data_file.path):
            instance.data_file.delete(False)