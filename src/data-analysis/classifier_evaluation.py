import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the dataset
df = pd.read_csv("filtered_file2.csv")  # Replace with actual file path

# Drop rows where the target variable is missing
df = df.dropna(subset=["STEM_Category"])

# Encode target variable (STEM_Category)
label_encoder = LabelEncoder()
df["STEM_Category_Encoded"] = label_encoder.fit_transform(df["STEM_Category"])

# Combine text-based features
df["Text_Features"] = df["Title"] + " " + df["Abstract"] + " " + df["Keywords"]

# Apply TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
X_tfidf = tfidf.fit_transform(df["Text_Features"])

# Initialize an empty list to store cluster labels
cluster_labels = pd.Series(index=df.index, dtype=int)

# Define the number of clusters per STEM category
num_clusters = 3  # Can be adjusted based on dataset size

# Apply K-Means clustering within each STEM category
for category in df["STEM_Category"].unique():
    # Filter data for the specific category
    category_indices = df[df["STEM_Category"] == category].index
    category_data = X_tfidf[category_indices]

    # Ensure we have enough samples for clustering
    if len(category_indices) >= num_clusters:
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        cluster_labels.loc[category_indices] = kmeans.fit_predict(category_data)
    else:
        cluster_labels.loc[category_indices] = 0  # Assign a single cluster if not enough samples

# Add cluster labels as a new feature
df["Cluster_Label"] = cluster_labels

# Prepare dataset for Multinomial Logistic Regression
X = pd.concat([pd.DataFrame(X_tfidf.toarray()), df["Cluster_Label"]], axis=1)
# Convert column names to strings
X.columns = X.columns.astype(str)  # This line is added
y = df["STEM_Category_Encoded"]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train the Multinomial Logistic Regression model
model = LogisticRegression(multi_class="multinomial", solver="newton-cg", max_iter=500)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Generate classification report
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

# Confusion Matrix visualization
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap='Blues', xticks_rotation='vertical')
plt.title("Confusion Matrix")
plt.show()

# Display the results
print(report)