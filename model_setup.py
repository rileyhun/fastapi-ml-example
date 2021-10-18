from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn import datasets
from sklearn.model_selection import train_test_split
import joblib

dataset = datasets.load_wine()

X = dataset.data
y = dataset.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

model = MultinomialNB()
model.fit(X_train, y_train)
predicted_y = model.predict(X_test)

joblib.dump(model, 'model.pkl')

print(metrics.classification_report(y_test, predicted_y, target_names=dataset.target_names))
