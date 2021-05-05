import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

import graphviz
from sklearn import tree
def show_decision_tree(clf, data_feature_names, data_target_names, name=""):
    """This function visualize a decision tree"""
    dot_data = tree.export_graphviz(clf, out_file=None) 
    graph = graphviz.Source(dot_data)
    graph.render(name) 
    dot_data = tree.export_graphviz(clf,                                    
                                    out_file=None,  
                                    filled=True,
                                    feature_names=data_feature_names,  
                                    class_names=data_target_names,
                                    rounded=True,  
                                    special_characters=True)  
    graph = graphviz.Source(dot_data)  
    return graph

#Initial values for our dataset
labels = ["balanced", "electric_fault", "unbalanced"]
labelsEncoded = {"balanced" : 0, "electric_fault" : 1, "unbalanced" : 2}
speeds = range(75, 105, 5) #75, 80, ..., 100

timeserieTable = []

for label in labels:
    for speed in speeds :
        timeseries = pd.read_csv(f"C:\\DEV\\IA\\TP3_machinelearning\\dataset_SOON_Electric_Engine_Simulator\\2021-03-26\\gray_{speed}_{label}.csv", header=None, names=["a1", "a2", "a3"])

        """
        settings = MinimalFCParameters()
        extract_features(timeseries, default_fc_parameters=settings, column_id="id")

        print(extracted_features)"""

        #Hand-made extraction
        # Unique parameters
        rollingWindow = 500

        #Speed
        timeseries["label"] = labelsEncoded[label]
        #Label encoding
        timeseries["speed"] = speed
        
        maxValues = {"a1" : np.max(np.abs(timeseries["a1"])), "a2" : np.max(np.abs(timeseries["a2"])), "a3" : np.max(np.abs(timeseries["a3"]))}
        # Parameters across accelerations
        for acc in ["a1", "a2", "a3"] :
            #Normalization 
            #timeseries[f"norm_{acc}"] = np.abs(timeseries[acc]) / maxValues[acc]
            timeseries[f"mean_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).mean()
            timeseries[f"std_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).std()
            timeseries[f"min_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).min()
            timeseries[f"max_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).max()

        #Calculate mean acceleration accross all accelerations
        #timeseries["Mean_accelerations"] = (timeseries["norm_a1"] + timeseries["norm_a2"] + timeseries["norm_a3"]) / 3

        #Delete lines with none values due to rolling window
        first_idx = timeseries['mean_a1'].first_valid_index()
        last_idx = timeseries['mean_a1'].last_valid_index()
        timeseries = timeseries.iloc[first_idx:last_idx]

        #print(timeseries)

        timeserieTable.append(timeseries)

#print("Printing all timeseries")
#print(timeserieTable)

proportionTest = 0.3

timeserieTestTable = []
timeserieTrainTable = []

#Prepare data
for timeserie in timeserieTable :
    #Remove 'working' data not fed to the neural network
    timeserie.drop(columns=['a1', 'a2', 'a3'], inplace=True)
    #split into separate dataframes
    train, test = train_test_split(timeserie, test_size=proportionTest)
    #add to tables
    timeserieTrainTable.append(train)
    timeserieTestTable.append(test)

#Concat features and label, extract label
train = pd.concat(timeserieTrainTable)
y_train = np.asarray(train.pop('label')).astype(np.float32)
x_train = np.asarray(train).astype(np.float32)

test = pd.concat(timeserieTestTable)
y_test = np.asarray(test.pop('label')).astype(np.float32)
x_test = np.asarray(test).astype(np.float32)

featuresName = train.columns

#DECISION TREE 
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, plot_confusion_matrix
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline

#Grid Search
pipeline = Pipeline([
    ('tf', Normalizer()),
    ('clf', DecisionTreeClassifier()),
])

#To know what we can change in the gridsearch, 
#print(pipeline.get_params().keys())

# Gridsearch
parameters = {
    'tf__norm': ["l1", "l2", "max"],
    'clf__criterion': ['gini', 'entropy'],
    'clf__max_depth' : range(5,10),
}

gs_clf = GridSearchCV(pipeline, parameters, verbose=1, cv=5)
gs_clf.fit(x_train, y_train)

#Fetch best AI
bestModel = gs_clf.best_estimator_

gs_clf.best_score_
print("...Estimating best parameters...")
for param_name in sorted(parameters.keys()):
    print(f"Best value for param {param_name} : {gs_clf.best_params_[param_name]}")


#Print gridsearch final accuracy
y_pred = bestModel.predict(x_test)
print(classification_report(y_test, y_pred))
plot_confusion_matrix(bestModel, x_test, y_test, cmap=plt.cm.Blues, values_format="3.0f")
plt.show()

#Show the decision tree obtained by the best model
#construct the decision tree according to best params and print it
""""
#Carefull : Doens't seem to work
bestDecisionTree = Pipeline([
    ('tf', Normalizer(norm=gs_clf.best_params_["tf__norm"])),
    ('clf', DecisionTreeClassifier(max_depth=gs_clf.best_params_["clf__max_depth"], criterion=gs_clf.best_params_["clf__criterion"])),
])
bestDecisionTree.fit(x_train, y_train)
show_decision_tree(bestDecisionTree, featuresName, labels, "./graph")
plt.show()"""