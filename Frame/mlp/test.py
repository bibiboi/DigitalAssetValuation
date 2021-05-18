from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
clf = MLPRegressor()
print(type(clf))
clf.score()
