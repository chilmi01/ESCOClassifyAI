import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

file_path = "filtered_file2.csv"  # Replace with the actual path
df = pd.read_csv(file_path)

# Processing categorical data (Label Encoding)
categorical_cols = ["Department", "Degree"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Processing textual data (TF-IDF for FoundSkills & FoundOccupations)
vectorizers = {}
text_cols = ["FoundSkills", "FoundOccupations"]
for col in text_cols:
    df[col] = df[col].fillna("").astype(str)  # Convert all values to string
    df[col] = df[col].apply(lambda x: x.replace(",", " "))  # Replace "," with space for proper tokenization
    vectorizer = TfidfVectorizer(max_features=100)  # Keep the 100 most important words
    transformed = vectorizer.fit_transform(df[col])
    vectorizers[col] = vectorizer
    df = pd.concat([df, pd.DataFrame(transformed.toarray(), columns=[f"{col}_{i}" for i in range(100)])], axis=1)

# Feature preparation & target variable
X = df.drop(columns=["_id", "Title", "Author", "Abstract", "Keywords", "Date", "FoundSkills", "FoundOccupations", "STEM_Category"])  # Remove non-useful columns
y = LabelEncoder().fit_transform(df["STEM_Category"])  # Encode STEM category

# Apply LDA for dimensionality reduction to 2D
lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit_transform(X, y)

# Visualization of the data
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y, cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label="STEM Category")
plt.xlabel("LDA Component 1")
plt.ylabel("LDA Component 2")
plt.title("LDA Projection of Thesis Data")
plt.show()


