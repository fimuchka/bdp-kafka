import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier

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

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test_1 = sc.transform(X_test_1)
X_test_2 = sc.transform(X_test_2)


clf = DecisionTreeClassifier(criterion='gini', splitter='random')
clf.fit(X_train, y_train)

y_pred_dt_1 = clf.predict(X_test_1)
#print y_pred_dt_1

y_pred_dt_2 = clf.predict(X_test_2)
#print y_pred_dt_2

cm_1_dt = confusion_matrix(y_test_1, y_pred_dt_1)
#print cm_1_dt

cm_2_dt = confusion_matrix(y_test_2, y_pred_dt_2)
#print cm_2_dt


# Pickling model
filename = "Decision Tree.pkl"
pickle.dump(clf, open(filename, 'wb'))

# Load model for reuse
loaded_model = pickle.load(open(filename, 'rb'))
y_pred_1 = loaded_model.predict(X_test_1)
y_pred_2 = loaded_model.predict(X_test_2)
print(y_pred_1, y_pred_2)
