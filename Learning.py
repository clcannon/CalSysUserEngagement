from numpy.lib.function_base import rot90
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lazypredict.Supervised import LazyClassifier, LazyRegressor


def trainall(X_train, X_test, y_train, y_test):
    # fit all models
    clf = LazyClassifier(verbose = 0, predictions=True)
    # models is a dataframe, predictions are predictions
    models, predictions = clf.fit(X_train, X_test, y_train, y_test) 
    # print(models,predictions)
    print(models)