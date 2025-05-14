import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load phishing dataset
df = pd.read_csv("phishing_dataset.csv")  # Use UCI or custom dataset
X = df.drop('phishing', axis=1)
y = df['phishing']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Save model
joblib.dump(clf, 'phishing_model.pkl')
