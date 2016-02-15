# Python
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import User
from django.db import models

# Third-party app imports

# Local app imports
from ontologies.models import OntologyTerm
from publications.models import Publication

#####################################################################################################
#  Project
#####################################################################################################
"""
 Class to hold Project information
"""
class ProjectManager(models.Manager):
    def get_queryset_publishable(self):
        return super(ProjectManager, self).get_queryset().filter(publishable=True).order_by('name')

    def get_queryset_allowed_projects(self, user):
        return super(ProjectManager, self).get_queryset().filter(contributors__id__exact=user.id).order_by('name')

    def get_queryset_projects_count(self, user):
        return super(ProjectManager, self).get_queryset().filter(contributors__id__exact=user.id).count()

class Project(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    description	= models.TextField(blank=True)
    experimental_approaches = models.TextField(blank=True)
    data_generation = models.TextField(blank=True)
    publishable = models.BooleanField(default=False)
    date_created = models.DateField(null=False)
    date_embargo = models.DateField(null=False)
    # Relationships
    contributors = models.ManyToManyField(User, through='ProjectContributor', related_name="%(app_label)s_%(class)s_contributors")
    publications = models.ManyToManyField(Publication, related_name="%(app_label)s_%(class)s_publications")

    # Managers
    objects = models.Manager() # The default manager.
    project_objects = ProjectManager() # The Project-specific manager.

    def __unicode__(self):
        return u"""{name}""".format(
            name=self.name,
        )

    def create_date(self):
        self.date_created = datetime.now()
        self.date_embargo = datetime.now() + timedelta(days=(1*365))

"""
 Class to hold Project to User relationship information
"""
class ProjectContributorManager(models.Manager):
    def create_project_as_superuser(self, project, user):
        project_contributor = self.create(project=project, user=user, super_user=True, date_joined=datetime.now())
        return project_contributor

class ProjectContributor(models.Model):
    project = models.ForeignKey(Project, null=False, related_name="%(app_label)s_%(class)s_project")
    user = models.ForeignKey(User, null=False, related_name="%(app_label)s_%(class)s_user")
    super_user = models.BooleanField(default=False) # access level
    date_joined = models.DateField(null=False)

    # Managers
    objects = models.Manager() # The default manager.
    project_contributor_objects = ProjectContributorManager() # The ProjectContributors-specific manager.

    class Meta:
        unique_together = ('project', 'user')

    def __unicode__(self):
        return u"""{user} in {project}""".format(
            project=self.project,
            user=self.user,
        )

    def create_date(self):
        self.date_joined = datetime.now()

    def get_super_user_status(self):
        return self.super_user