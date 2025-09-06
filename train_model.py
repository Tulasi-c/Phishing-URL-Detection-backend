import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
data = pd.read_csv("urls_labels.csv")

print("Columns:", data.columns)
print(data.head())

# Features and labels
X = data['url']
y = data['label']  # Already numeric: 0 = safe, 1 = phishing

# Convert URLs into numerical features using n-grams
vectorizer = CountVectorizer(ngram_range=(1, 3))
X = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train model with class weight to handle imbalance
model = LogisticRegression(max_iter=200, class_weight='balanced')
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained and saved as model.pkl and vectorizer.pkl")


