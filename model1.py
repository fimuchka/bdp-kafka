from __future__ import division, print_function, unicode_literals

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import time
import pickle

'''
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.svm import SVC
'''

datapath = "/Users/jessiefan/Downloads/"
data = pd.read_csv(datapath+"creditcard.csv", thousands=',')

# Learn data (data structure)
# print(data.info())
# print(data.columns)

# Data Modeling
# Features selection
features = data.columns[:]
X = StandardScaler().fit_transform(data[features])
y = data['Class'].ravel()

# Split data using train_test_split function
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

names = [
    #"Naive Bayes",
    #"Logistic",
    #"Gradient Descent",
    #"Perceptron",
    #"Neural Network",
    "Decision Tree",
    #"Random Forest",
    #"AdaBoost",
    #"Gradient Boosting",
    #"Bagging",
    #"SVM-RBF"
]

# Create a list for all classifiers
# parameter setting shown in list are the combinations where I found optimum accuracy at

classifiers = [
    #BernoulliNB(binarize=-0.05),
    #LogisticRegression(),
    #SGDClassifier(),
    #Perceptron(penalty='l1', alpha=0.00011),
    #MLPClassifier(activation='identity'),
    DecisionTreeClassifier(criterion='gini', splitter='random'),
    #RandomForestClassifier(n_estimators=100, criterion='entropy', bootstrap=False),
    #AdaBoostClassifier(n_estimators=50, learning_rate=1.1),
    #GradientBoostingClassifier(loss='deviance', learning_rate=0.18, n_estimators=150),
    #BaggingClassifier(n_estimators=50),
    #SVC(kernel='rbf'),
]

# The following for loop will iterate through lists of names and classifiers

for name, clf in zip(names, classifiers):
    start_time = time.time()
    clf.fit(X_train, y_train)
    predicted_IV = clf.predict(X_test)
    score = clf.score(X_test, y_test)
    end_time = time.time()
    print(name, ':', format(score, '.3f'), '|time elapsed:', format((end_time - start_time), '.2f'), '\n')

# Pickling model
filename = "model1.pkl"
pickle.dump(clf, open(filename, 'wb'))

# Load model for reuse
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)