# -*- coding: utf-8 -*-
"""ML_Code_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oZ3ry7TPnO7qoCxA7IRj-Om_XrrOcCY6
"""

import csv
import os
import re
import sys
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import statistics
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from collections import Counter


class Classification:
    def __init__(self, path='/home/iiserb/ML_Project_test_1/training_data_resampled.csv', clf_opt='lr', no_of_selected_features=None):
        self.path = path
        self.clf_opt = clf_opt
        self.no_of_selected_features = no_of_selected_features
        if self.no_of_selected_features is not None:
            self.no_of_selected_features = int(self.no_of_selected_features)

    # Selection of classifiers
    def classification_pipeline(self):
        # AdaBoost
        if self.clf_opt == 'ab':
            print('\n\t### Training AdaBoost Classifier ### \n')
            be1 = svm.SVC(kernel='linear', class_weight='balanced', probability=True)
            be2 = LogisticRegression(solver='liblinear', class_weight='balanced')
            be3 = DecisionTreeClassifier(max_depth=50)
            clf = AdaBoostClassifier(algorithm='SAMME.R', n_estimators=100)
            clf_parameters = {
                'clf__base_estimator': (be1, be2, be3),
                'clf__random_state': (0, 10),
            }
        # Decision Tree
        elif self.clf_opt == 'dt':
            print('\n\t### Training Decision Tree Classifier ### \n')
            clf = DecisionTreeClassifier(random_state=40)
            clf_parameters = {
                'clf__criterion': ('gini', 'entropy'),
                'clf__max_features': ('auto', 'sqrt', 'log2'),
                'clf__max_depth': (10, 40, 45, 60),
                'clf__ccp_alpha': (0.009, 0.01, 0.05, 0.1),
            }
        # Logistic Regression
        elif self.clf_opt == 'lr':
            print('\n\t### Training Logistic Regression Classifier ### \n')
            clf = LogisticRegression(solver='liblinear', class_weight='balanced')
            clf_parameters = {
                'clf__random_state': (0, 10),
            }
        # Multinomial Naive Bayes
        elif self.clf_opt == 'nb':
            print('\n\t### Training Multinomial Naive Bayes Classifier ### \n')
            clf = MultinomialNB(fit_prior=True, class_prior=None)
            clf_parameters = {
                'clf__alpha': (0, 1),
            }
        # Random Forest
        elif self.clf_opt == 'rf':
            print('\n\t ### Training Random Forest Classifier ### \n')
            clf = RandomForestClassifier(max_features=None, class_weight='balanced')
            clf_parameters = {
                'clf__criterion': ('entropy', 'gini'),
                'clf__n_estimators': (30, 50, 100),
                'clf__max_depth': (10, 20, 30, 50, 100, 200),
            }
        # Support Vector Machine
        elif self.clf_opt == 'svm':
            print('\n\t### Training SVM Classifier ### \n')
            clf = svm.SVC(class_weight='balanced', probability=True)
            clf_parameters = {
                'clf__C': (0.1, 1, 100),
                'clf__kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
            }
        else:
            print('Select a valid classifier \n')
            sys.exit(0)
        return clf, clf_parameters

    # Statistics of individual classes
    def get_class_statistics(self, labels):
        class_statistics = Counter(labels)
        print('\n Class \t\t Number of Instances \n')
        for item in list(class_statistics.keys()):
            print('\t' + str(item) + '\t\t\t' + str(class_statistics[item]))

    # Load the data
    def get_data(self):
        # Load the file using Pandas
        reader = pd.read_csv(self.path)
        data = reader.iloc[:, :-1]
        labels = reader['target']
        self.get_class_statistics(labels)
        # Training and Test Split
        training_data, validation_data, training_cat, validation_cat = train_test_split(
            data, labels, test_size=0.05, random_state=42, stratify=labels
        )
        return training_data, validation_data, training_cat, validation_cat

    # Classification using the Gold Standard after creating it from the raw text
    def classification(self):
        # Get the data
        training_data, validation_data, training_cat, validation_cat = self.get_data()

        clf, clf_parameters = self.classification_pipeline()
        pipeline = Pipeline(
            [
                ('feature_selection', SelectKBest(chi2, k=self.no_of_selected_features)),
                ('clf', clf),
            ]
        )
        grid = GridSearchCV(pipeline, clf_parameters, scoring='f1_macro', cv=5)
        grid.fit(training_data, training_cat)
        clf = grid.best_estimator_
        print('\n\n The best set of parameters of the pipiline are: ')
        print(clf)
        joblib.dump(clf, self.path + 'training_model.joblib')
        predicted = clf.predict(validation_data)

        # Evaluation
        class_names = list(Counter(validation_cat).keys())
        class_names = [str(x) for x in class_names]

        # Confusion Matrix
        print('\n *************** Confusion Matrix ***************  \n')
        print(confusion_matrix(validation_cat, predicted))

        # Classification Report
        print('\n ##### Classification Report ##### \n')
        print(classification_report(validation_cat, pred# Get the estimated coefficients
params = tobit_res.params

# Add a column of ones for the intercept
exog_with_intercept = sm.add_constant(exog)

# Ensure the number of features matches the number of coefficients
if exog_with_intercept.shape[1] != len(params):
    raise ValueError("Number of features does not match the number of coefficients.")

# Manually calculate predictions
predictions = np.dot(exog_with_intercept, params)

# Model Performance Metrics
mse = mean_squared_error(df['secchi_depth'], predictions)
r_squared = r2_score(df['secchi_depth'], predictions)

print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared: {r_squared:.4f}")

print(tobit_res.summary())
print(exog_with_intercept.columns)



# Residual Analysis
residuals = tobit_res.resid
plt.scatter(predictions, residuals, color='skyblue', s=10)
plt.title('Residuals vs Predictions')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.show()

# Distribution of Residuals
plt.hist(residuals, bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

# Predicted vs. Observed Values
plt.scatter(predictions, df['secchi_depth'], color='skyblue', s=10)
plt.plot([min(predictions), max(predictions)], [min(predictions), max(predictions)], linestyle='--', color='red', linewidth=2)
plt.title('Predicted vs. Observed Values')
plt.xlabel('Predicted Values')
plt.ylabel('Observed Values')
plt.show()
icted, target_names=class_names))

        pr = precision_score(validation_cat, predicted, average='macro')
        print('\n Precision:\t' + str(pr))

        rl = recall_score(validation_cat, predicted, average='macro')
        print('\n Recall:\t' + str(rl))

        fm = f1_score(validation_cat, predicted, average='macro')
        print('\n F1-Score:\t' + str(fm))


# Example usage:
classifier = Classification(clf_opt='rf', no_of_selected_features=10)
classifier.classification()

