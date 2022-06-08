import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import pickle
from scipy.stats import shapiro


# Read file
df = pd.read_csv("ObesityDataSet_raw_and_data_sinthetic.csv")



#Drop Height and Weight because it correlate to BMI calculate
df = df.drop(columns=['Height', 'Weight'])
print(df.shape)

#No null values
df[df.isnull().any(axis=1)]

# Convert object/text variables to category variables
columns = ["Gender", "family_history_with_overweight", "FAVC", "CAEC", "SMOKE", "SCC", "CALC", "MTRANS", "NObeyesdad"]

for col in columns:
    df[col] = df[col].astype('category')

# function to interigate data after conversion
# provides min, max, unique counts
def variable_counts(columns, stage):

    if stage == 'pre':
        print("Pre Conversion to Integer")
    else:
        print("Post Conversion to Integer")

    for col in columns:
        print("Variable:", col, "| Count Unique:",df[col].nunique(),"| Min: ", df[col].min(), "| Max: ",df[col].max())


# Convert float variables to integer to the nearest inter
columns = ["FCVC", "NCP", "CH2O", "TUE", "FAF"]

# pre conversion countss
variable_counts(columns, 'pre')

# convert to int / nearest int value
for col in columns:
    # round to nearest whole number
    df[col] = round(df[col]).astype('int')

# post conversion counts
print("")
variable_counts(columns, 'post')

df_prep = df.copy()

df_prep = pd.get_dummies(df_prep,columns=["Gender","family_history_with_overweight",
                                          "FAVC","CAEC","SMOKE","SCC","CALC","MTRANS"])
print(df_prep.head())
print(df_prep.shape)
for col in df_prep.columns:
    print(col)
# split dataset in features and target variable

# Features
X = df_prep.drop(columns=["NObeyesdad"])

# Target variable
y = df_prep['NObeyesdad']

# import sklearn packages for data treatments
from sklearn.model_selection import train_test_split # Import train_test_split function

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation
from sklearn.preprocessing import StandardScaler  # Import for standard scaling of the data
from sklearn.preprocessing import MinMaxScaler  # Import for standard scaling of the data

# standard scale data
ss = StandardScaler()
X_train_scaled = ss.fit_transform(X_train)
X_test_scaled = ss.transform(X_test)

print(X_test_scaled)


# tested MinMaxScaler as KNN historically does better with MinMax
mm = MinMaxScaler()
X_train_mm_scaled = ss.fit_transform(X_train)
X_test_mm_scaled = ss.transform(X_test)


# program to run multilple models though sklearn
# Default settings output accuracy and classification report
# compares accuracy for scaled and unscaled data
def run_models(X_train: pd.DataFrame, y_train: pd.DataFrame, X_test: pd.DataFrame, y_test: pd.DataFrame):
    models = [
        ('Random Forest', RandomForestClassifier(random_state=2020)),
        ('Decision Tree', DecisionTreeClassifier()),
        ('KNN', KNeighborsClassifier()),
        ('SVM', SVC())
    ]

    for name, model in models:
        # unscaled data
        clf = model.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        # scaled data
        clf_scaled = model.fit(X_train_scaled, y_train)
        y_pred_scaled = clf_scaled.predict(X_test_scaled)

        # mm scaled data
        clf_mm_scaled = model.fit(X_train_mm_scaled, y_train)
        y_pred_mm_scaled = clf_scaled.predict(X_test_mm_scaled)

        # accuracy scores
        accuracy = round(metrics.accuracy_score(y_test, y_pred), 5)
        scaled_accuracy = round(metrics.accuracy_score(y_test, y_pred_scaled), 5)
        scaled_mm_accuracy = round(metrics.accuracy_score(y_test, y_pred_mm_scaled), 5)

        # output
        print(name + ':')
        print("---------------------------------------------------------------")
        print("Accuracy:", accuracy)
        print("Accuracy w/Scaled Data (ss):", scaled_accuracy)
        print("Accuracy w/Scaled Data (mm):", scaled_mm_accuracy)
        if (accuracy > scaled_accuracy) and (accuracy > scaled_mm_accuracy):
            print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred))
            print("                            -----------------------------------               \n")
        elif (scaled_accuracy > scaled_mm_accuracy):
            print("\nClassification Report (ss):\n", metrics.classification_report(y_test, y_pred_scaled))
            print("                            -----------------------------------               \n")
        else:
            print("\nClassification Report (mm):\n", metrics.classification_report(y_test, y_pred_mm_scaled))
            print("                            -----------------------------------               \n")

#run Decision Trees, Random Forest, KNN and SVM
run_models(X_train, y_train, X_test, y_test)

from sklearn.model_selection import GridSearchCV


# model name, classifier, parameters
# function used to process models and parameters through gridsearch
def hyper_tune(name, clf, parameters, target_names=None):
    target_names = target_names
    clf = clf
    search = GridSearchCV(clf, parameters, verbose=True, n_jobs=15, cv=5)
    search.fit(X_train_scaled, y_train)
    y_pred_scaled = search.predict(X_test_scaled)
    print("Accuracy Score = %3.2f" % (search.score(X_test_scaled, y_test)))
    print(search.best_params_)
    print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred_scaled, target_names=target_names))


# the KNN model performs better on the unscaled data this function
# function for unscaled data
# model name, classifier, parameters
# function used to process models and parameters through gridsearch
def hyper_tune2(name, clf, parameters, target_names=None):
    target_names = target_names
    clf = clf
    search = GridSearchCV(clf, parameters, verbose=True, n_jobs=15, cv=5)
    search.fit(X_train, y_train)
    y_pred = search.predict(X_test)
    print("Accuracy Score = %3.2f" % (search.score(X_test, y_test)))
    print(search.best_params_)
    print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred, target_names=target_names))


# Number of neighbors
n_neighbors = [int(x) for x in range(4, 15)]
# weights
weights = ['uniform','distance']
# distance metric
metric = ['euclidean', 'manhattan', 'chebyshev']
# computation algorithm
algorithm = ['auto', 'ball_tree', 'kd_tree', 'brute']
# power paramter
p=[1,2]

parameters = { 'n_neighbors': n_neighbors,
              'weights':weights,
              'metric':metric,
              'p':p,
              'algorithm': algorithm
               }

hyper_tune2('KNN', KNeighborsClassifier(), parameters)



# Number of trees in random forest
n_estimators = [int(x) for x in range(10, 200,10)]
# Criterion
criterion = ['gini','entropy']
# Number of features to consider at every split
max_features = ['auto', 'sqrt', 'log2']
# Maximum number of levels in tree
max_depth = [int(x) for x in range(10, 100, 10)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [int(x) for x in range(2, 5)]
# Minimum number of samples required at each leaf node
min_samples_leaf = [int(x) for x in range(2, 5)]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# random state
random_state = [1010]

parameters = { 'criterion':criterion,
               'n_estimators': n_estimators,
              'max_depth':max_depth,
              #'random_state': random_state,
              #'max_features':max_features,
              #'min_samples_split':min_samples_split
               }


hyper_tune('Random Forest',
           RandomForestClassifier(), parameters)


# Create Decision Tree classifer object with optimized parameters
clf = RandomForestClassifier(criterion='entropy',
               n_estimators=52,
              max_depth = 51,
              max_features='auto',
              min_samples_split=2,
              random_state=1010)

# Train Decision Tree Classifer
clf = clf.fit(X_train_scaled, y_train)


filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))
#Predict the response for test dataset
y_pred = clf.predict(X_test_scaled)
print(X.columns)
print(y_pred)



