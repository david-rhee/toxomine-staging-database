# Python imports
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Local app imports
from projects.models import Project, ProjectContributor

######################################################################################################
##  Get or Create Project
######################################################################################################
def get_project(name, description, experimental_approaches, data_generation, publishable, user, publication_list):
    #check if project exist, if so return, if not create new
    try:
        year_later = datetime.now() + timedelta(days=(1*365))
        project = Project(name=name, description=description, experimental_approaches=experimental_approaches, data_generation=data_generation,
                          publishable=publishable, date_created=datetime.now(), date_embargo=year_later)
        project.validate_unique()
        project.save()
        
        for publication in publication_list:
            project.publications.add(publication)

        project_contributor = ProjectContributor.project_contributor_objects.create_project_as_superuser(project, user)
        project_contributor.validate_unique()
        project_contributor.save()

    except ValidationError as e:
        project = Project.objects.get(name=name)

    return project

######################################################################################################
##  Get or Create ProjectContributor
######################################################################################################
def add_project_contributor(project, user):
    try:
        project_contributor = ProjectContributor(project=project, user=user, super_user='True', date_joined=datetime.now())
        project_contributor.validate_unique()
        project_contributor.save()

    except ValidationError as e:
        project_contributor = ProjectContributor.objects.get(project=project, user=user)

    return project_contributor