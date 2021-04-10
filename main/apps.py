import glob
import os

from keras.models import load_model
import joblib

from django.apps import AppConfig
from sklearn.preprocessing import MinMaxScaler


class MainConfig(AppConfig):
    name = 'main'
    dse_models = {}
    for filepath in glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/dse_estimator/models/*.model')[: 20]:
        print((filepath.split('/')[-1]).split('.')[0])
        dse_models[(filepath.split('/')[-1]).split('.')[0]] = load_model(filepath)

    minmax_scalers = {}
    for filepath in glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/dse_estimator/scalers/*.pkl')[: 20]:
        minmax_scalers[(filepath.split('/')[-1]).split('.')[0]] = joblib.load(open(filepath, 'rb'))
