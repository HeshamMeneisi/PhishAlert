from scipy.io import arff
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPRegressor
import pickle, os.path

pickled_file = 'model.pyo'

data = arff.loadarff("Training Dataset.arff")

score_func = recall_score

meta = data[1]
data = data[0]
print(meta)
example_count = len(data)
field_count = len(data[0]) - 1

X = np.zeros((example_count, field_count))
y = np.zeros(example_count)
for i in range(example_count):
    for j in range(field_count):
        X[i, j] = data[i][j]
        y[i] = data[i][-1]


X = np.concatenate((X[:, 0:9], X[:, 11].reshape(-1, 1)), axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

# TODO: Replace this with a proper grid search with k-folds
a0 = 0
if os.path.exists(pickled_file):
    last_model = pickle.load(open(pickled_file, 'rb'))
    a0 = score_func(y_test, (last_model.predict(X_test) > 0) * 2 - 1)
print("Current Best:", a0)

cl1 = GradientBoostingClassifier()
cl1.fit(X_train, y_train)
a1 = score_func(y_test, (cl1.predict(X_test)>0)*2-1)
print("GB: ", a1)

cl2 = LogisticRegression()
cl2.fit(X_train, y_train)
a2 = score_func(y_test, (cl2.predict(X_test)>0)*2-1)
print("LR: ", a2)

cl3 = SVC(kernel = 'rbf', gamma = 100)
cl3.fit(X_train, y_train)
a3 = score_func(y_test, cl3.predict(X_test))
print("SVM: ", a3)

cl4 = MLPRegressor(activation='tanh', tol=1e-10, hidden_layer_sizes=(5, 5))
cl4.fit(X_train, y_train)
a4 = score_func(y_test, (cl4.predict(X_test)>0)*2-1)
print("MLP: ", a4)

new_best = None
if a1 > a0:
    a0 = a1
    new_best = cl1
if a2 > a0:
    a0 = a2
    new_best = cl2
if a3 > a0:
    a0 = a3
    new_best = cl3
if a4 > a0:
    a0 = a4
    new_best = cl4

if new_best:
    print("New Best:", a0)
    pickle.dump(cl1, open(pickled_file, 'wb'))
