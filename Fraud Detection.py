import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

datapath = "/Users/jessiefan/Downloads/"


# define X_train, y_train
dataset_train = pd.read_csv(datapath+'training.csv', thousands=',')
X_train = dataset_train.iloc[:, 1:30].values
y_train = dataset_train.iloc[:, 30].values

# define X_test_1, y_test_1
dataset_test_1 = pd.read_csv(datapath+'test_01.csv', thousands=',')
X_test_1 = dataset_test_1.iloc[:, 1:30].values
y_test_1 = dataset_test_1.iloc[:, 30].values

# define X_test_2, y_test_2
dataset_test_2 = pd.read_csv(datapath+'test_02.csv', thousands=',')
X_test_2 = dataset_test_2.iloc[:, 1:30].values
y_test_2 = dataset_test_2.iloc[:, 30].values

dataset_train.shape
dataset_train.head()

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test_1 = sc.transform(X_test_1)
X_test_2 = sc.transform(X_test_2)

classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)

y_pred_1 = classifier.predict(X_test_1)
print y_pred_1

y_pred_2 = classifier.predict(X_test_2)
print y_pred_2

from sklearn.metrics import confusion_matrix
cm_1 = confusion_matrix(y_test_1, y_pred_1)
print cm_1

error_1=(68862+73)/(68862+73+14+34)
print error_1

cm_2 = confusion_matrix(y_test_2, y_pred_2)
print cm_2

error_2=(48187+60)/(48187+60+12+29)
print error_2

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(criterion='gini', splitter='random')
clf.fit(X_train, y_train)

y_pred_dt_1 = clf.predict(X_test_1)
print y_pred_dt_1

y_pred_dt_2 = clf.predict(X_test_2)
print y_pred_dt_2

cm_1_dt = confusion_matrix(y_test_1, y_pred_dt_1)
print cm_1_dt

cm_2_dt = confusion_matrix(y_test_2, y_pred_dt_2)
print cm_2_dt

# Pickling model
filename = "Fraud Detection.pkl"
pickle.dump(clf, open(filename, 'wb'))

# Load model for reuse
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test_1, y_test_1)
result = loaded_model.score(X_test_2, y_test_2)
print(result)
