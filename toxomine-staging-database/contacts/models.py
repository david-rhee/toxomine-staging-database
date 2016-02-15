# Python
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import User
from django.db import models

# Third-party app imports

# Local app imports

######################################################################################################
##  Lab and User
######################################################################################################
"""
 Class to hold Lab information
"""
class Lab(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    pi_first_name = models.CharField(max_length=50, blank=False)
    pi_last_name = models.CharField(max_length=50, blank=False)
    affiliation = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    #Relationships
    lab_members = models.ManyToManyField(User, through='LabMember', related_name="%(app_label)s_%(class)s_lab_members")

    def __unicode__(self):
        return u"""{name}""".format(name=self.name)

"""
 Class to hold Lab to User relationship information
"""
class LabMemberManager(models.Manager):
    def create_lab_as_superuser(self, lab, user):
        lab_member = self.create(lab=lab, user=user, super_user=True, date_joined=datetime.now())
        return lab_member

"""
 Class to hold User to Lab relationship information
"""
class LabMember(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=False, related_name="%(app_label)s_%(class)s_lab")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="%(app_label)s_%(class)s_user")
    super_user = models.BooleanField(default=False) # access level
    date_joined = models.DateField(null=False)

    # Managers
    objects = models.Manager() # The default manager.
    lab_member_objects = LabMemberManager() # The LabMember-specific manager.

    class Meta:
        unique_together = ('lab', 'user')

    def __unicode__(self):
        return u"""{user} in {lab}""".format(user=self.user, lab=self.lab)

    def create_date(self):
        self.date_joined = datetime.now()

    def get_super_user_status(self):
        return self.super_user