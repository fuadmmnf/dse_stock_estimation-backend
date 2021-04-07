import glob
from keras.models import load_model

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    dse_models = {}

    for filepath in glob.iglob('dse_estimator/models/**'):
        dse_models[(filepath.split('/')[-1])] = load_model(filepath)
