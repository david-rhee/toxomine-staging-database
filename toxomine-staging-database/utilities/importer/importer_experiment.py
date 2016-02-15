# Python imports
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Local app imports
from experiments.models import Experiment, ExperimentContributor

######################################################################################################
##  Get or Create Experiment
######################################################################################################
def get_experiment(name, description, category, publishable, user, project, publication_list):
    #check if experiment exist, if so return, if not create new
    try:
        year_later = datetime.now() + timedelta(days=(1*365))
        experiment = Experiment(name=name, description=description, category=category,
                                publishable=publishable, date_created=datetime.now(), date_embargo=year_later)
        experiment.validate_unique()
        experiment.save()
        
        experiment.projects.add(project)
        for publication in publication_list:
            experiment.publications.add(publication)

        experiment_contributor = ExperimentContributor.experiment_contributor_objects.create_experiment_as_superuser(experiment, user)
        experiment_contributor.validate_unique()
        experiment_contributor.save()

    except ValidationError as e:
        experiment = Experiment.objects.get(name=name)
  
    return experiment

######################################################################################################
##  Get or Create Experiment Contributor
######################################################################################################
def add_experiment_contributor(experiment, user):
    try:
        experiment_contributor = ExperimentContributor(experiment=experiment, user=user, super_user='True', date_joined=datetime.now())
        experiment_contributor.validate_unique()
        experiment_contributor.save()

    except ValidationError as e:
        experiment_contributor = ExperimentContributor.objects.get(experiment=experiment, user=user)

    return experiment_contributor