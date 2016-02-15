# Python
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.validators import ValidationError
from django.db import models

# Third-party app imports

# Local app imports
from experiments.models import Experiment
from ontologies.models import OntologyTerm
from protocols.models import Protocol
from publications.models import Publication

#####################################################################################################
#  Submission
#####################################################################################################
"""
 Class to hold Submission information
"""
class SubmissionManager(models.Manager):
    def get_queryset_publishable(self):
        return super(SubmissionManager, self).get_queryset().filter(publishable=True).order_by('name')

    def get_queryset_allowed_submissions(self, user):
        return super(SubmissionManager, self).get_queryset().filter(contributors__id__exact=user.id).order_by('name')

    def get_queryset_submissions_count(self, user):
        return super(SubmissionManager, self).get_queryset().filter(contributors__id__exact=user.id).count()

class Submission(models.Model):
    generated_id = models.CharField(max_length=255, null=False) # Datacore generated id: example TC1
    given_name = models.CharField(max_length=255, null=False) # User given name: example - GCN5B
    name = models.CharField(max_length=255, null=False, unique=True) # Combine generated id + given name: TC1_GCN5B
    description = models.TextField(blank=True)
    publishable = models.BooleanField(default=False)
    date_created = models.DateField(null=False)
    date_embargo = models.DateField(null=False)
    technique = models.ForeignKey(OntologyTerm, null=True, related_name="%(app_label)s_%(class)s_technique")
    quality_control = models.ForeignKey(OntologyTerm, null=True, related_name="%(app_label)s_%(class)s_quality_control")
    replicate_series = models.CharField(max_length=10, null=False)
    date_replicate = models.DateField(null=False)
    note = models.TextField(blank=True)
    #Relationships
    contributors = models.ManyToManyField(User, through='SubmissionContributor', related_name="%(app_label)s_%(class)s_contributors")
    experiments = models.ManyToManyField(Experiment, related_name="%(app_label)s_%(class)s_experiments")
    related_submissions = models.ManyToManyField('self', through='SubmissionSubmission', symmetrical=False, related_name="%(app_label)s_%(class)s_related_submissions")
    publications = models.ManyToManyField(Publication, blank=True, related_name="%(app_label)s_%(class)s_publications")

    # Managers
    objects = models.Manager() # The default manager.
    submission_objects = SubmissionManager() # The Submission-specific manager.

    def __unicode__(self):
        return u"""{name}""".format(
            name=self.name,
        )

    def create_date(self):
        self.date_created = datetime.now()
        self.date_embargo = datetime.now() + timedelta(days=(1*365))

    def get_date_replicate(self):
        return self.date_replicate.strftime('%m/%d/%Y')

"""
 Class to hold User to Submission relationship information
"""
class SubmissionContributorManager(models.Manager):
    def create_submission_as_superuser(self, submission, user):
        return self.create(submission=submission, user=user, super_user=True, date_joined=datetime.now())

class SubmissionContributor(models.Model):
    submission = models.ForeignKey(Submission, null=False, related_name="%(app_label)s_%(class)s_submission")
    user = models.ForeignKey(User, null=False, related_name="%(app_label)s_%(class)s_user")
    super_user = models.BooleanField(default=False) # access level
    date_joined = models.DateField(null=False)

    # Managers
    objects = models.Manager() # The default manager.
    submission_contributor_objects = SubmissionContributorManager() # The SubmissionContributors-specific manager.

    class Meta:
        unique_together = ('submission', 'user')

    def __unicode__(self):
        return u"""{user} in {submission}""".format(
            submission=self.submission,
            user=self.user,
        )

    def create_date(self):
        self.date_joined = datetime.now()

    def get_super_user_status(self):
        return self.super_user

"""
 Class to hold Submission to Submission relationship information
"""
class SubmissionSubmission(models.Model):
    submission_parent = models.ForeignKey(Submission, null=False, related_name="%(app_label)s_%(class)s_submission_parent")
    submission_child = models.ForeignKey(Submission, null=False, related_name="%(app_label)s_%(class)s_submission_child")
    date_linked = models.DateField(null=False)

    class Meta:
        unique_together = ('submission_parent', 'submission_child')

    def __unicode__(self):
        return u"""{submission_child} related to {submission_parent}""".format(
            submission_parent=self.submission_parent,
            submission_child=self.submission_child,
        )

    def create_date(self):
        self.date_linked = datetime.now()

    def validate_unique(self, *args, **kwargs):
        super(SubmissionSubmission, self).validate_unique(*args, **kwargs)
        if self.submission_parent == self.submission_child:
            raise ValidationError(
                    {
                        NON_FIELD_ERRORS:
                        ('Error --- Parent and Child same',)
                    }
                )

#####################################################################################################
#  AppliedProtocol
#####################################################################################################
"""
 Class to hold Applied Protocol information
"""
class AppliedProtocolManager(models.Manager):
    def submission(self, submission_id):
        return super(AppliedProtocolManager, self).get_queryset().filter(submission__id__exact=submission_id)

class AppliedProtocol(models.Model):
    step = models.PositiveIntegerField(default=1)
    #Relationships
    protocol = models.ForeignKey(Protocol, related_name="%(app_label)s_%(class)s_protocol")
    submission = models.ForeignKey(Submission, related_name="%(app_label)s_%(class)s_submission")
    previous_applied_protocol = models.ForeignKey("AppliedProtocol", null=True, related_name="%(app_label)s_%(class)s_previous_applied_protocol")

    # Managers
    objects = models.Manager() # The default manager.
    applied_protocol_objects = AppliedProtocolManager() # The AppliedProtocol-specific manager.

    def __unicode__(self):
        return u"""{step}""".format(step=self.step)

#####################################################################################################
#  SubmissionData
#####################################################################################################
"""
 Class to hold Submission Data information
"""
class SubmissionData(models.Model):
    series = models.PositiveIntegerField(default=1) #Defines which series
    #Relationships
    applied_protocol_input = models.ForeignKey(AppliedProtocol, null=True, blank=True, related_name="%(app_label)s_%(class)s_input")
    applied_protocol_output = models.ForeignKey(AppliedProtocol, null=True, blank=True, related_name="%(app_label)s_%(class)s_output")

    # Submission Properties    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')