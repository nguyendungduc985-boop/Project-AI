from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

rf_classifer = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifer.fit(X_train, y_train)
oob_accuracy = rf_classifer.oob_score_
print(f"Out-of-Bag Accuracy: {oob_accuracy:.2f}")

y_pred = rf_classifer.predict(X_test)   
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.2f}")
