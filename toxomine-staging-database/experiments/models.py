# Python
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import User
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm
from projects.models import Project
from publications.models import Publication

#####################################################################################################
#  Experiment
#####################################################################################################
"""
 Class to hold Experiment information
"""
class ExperimentManager(models.Manager):
    def get_queryset_publishable(self):
        return super(ExperimentManager, self).get_queryset().filter(publishable=True).order_by('name')

    def get_queryset_allowed_experiments(self, user):
        return super(ExperimentManager, self).get_queryset().filter(contributors__id__exact=user.id).order_by('name')

    def get_queryset_experiments_count(self, user):
        return super(ExperimentManager, self).get_queryset().filter(contributors__id__exact=user.id).count()

class Experiment(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(blank=True)
    publishable = models.BooleanField(default=False)
    date_created = models.DateField(null=False)
    date_embargo = models.DateField(null=False)
    category = models.ForeignKey(OntologyTerm, null=True, related_name="%(app_label)s_%(class)s_category")
    #Relationships
    contributors = models.ManyToManyField(User, through='ExperimentContributor', related_name="%(app_label)s_%(class)s_contributors")
    projects = models.ManyToManyField(Project, blank=True, related_name="%(app_label)s_%(class)s_projects")
    publications = models.ManyToManyField(Publication, blank=True, related_name="%(app_label)s_%(class)s_publications")

    # Managers
    objects = models.Manager() # The default manager.
    experiment_objects = ExperimentManager() # The Project-specific manager.

    def __unicode__(self):
        return u"""{name}""".format(
            name=self.name,
        )

    def create_date(self):
        self.date_created = datetime.now()
        self.date_embargo = datetime.now() + timedelta(days=(1*365))

"""
 Class to hold Experiment to User relationship information
"""
class ExperimentContributorManager(models.Manager):
    def create_experiment_as_superuser(self, experiment, user):
        experiment_contributor = self.create(experiment=experiment, user=user, super_user=True, date_joined=datetime.now())
        return experiment_contributor

class ExperimentContributor(models.Model):
    experiment = models.ForeignKey(Experiment, null=False, related_name="%(app_label)s_%(class)s_experiment")
    user = models.ForeignKey(User, null=False, related_name="%(app_label)s_%(class)s_user")
    super_user = models.BooleanField(default=False) # access level
    date_joined = models.DateField(null=False)

    # Managers
    objects = models.Manager() # The default manager.
    experiment_contributor_objects = ExperimentContributorManager() # The ExperimentContributors-specific manager.

    class Meta:
        unique_together = ('experiment', 'user')

    def __unicode__(self):
        return u"""{user} in {experiment}""".format(
            experiment=self.experiment,
            user=self.user,
        )

    def create_date(self):
        self.date_joined = datetime.now()

    def get_super_user_status(self):
        return self.super_user